from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

# Initialize Router
router = APIRouter()

# Get absolute path of the backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "cases_data.csv")
EMBEDDING_PATH = os.path.join(BASE_DIR, "data", "case_embeddings.npy")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "data", "case_embeddings.index")

# Load Data
try:
    df = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find cases_data.csv at {CSV_PATH}")

# Load FAISS Index & Embeddings
try:
    embeddings = np.load(EMBEDDING_PATH)
    index = faiss.read_index(FAISS_INDEX_PATH)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not load embeddings or FAISS index from {EMBEDDING_PATH} or {FAISS_INDEX_PATH}")

# Load SentenceTransformer Model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load LLM Model
llm = ChatGroq(model_name="mistral-saba-24b", temperature=0.3, groq_api_key=GROQ_API_KEY)

# Enhanced Prompt Template for Case Details (Restored "Case Breakdown")
prompt_template = """
You are a highly skilled legal analyst. Given the details of a court case, generate a well-structured breakdown in a professional and concise manner, including arguments, evidence, strength evaluation, and outcome analysis.

### *Case Breakdown*
- *Court:* {court_name}
- *Petitioner:* {petitioner}
- *Case Type:* {case_type}
- *Primary Legal Issue:* (Summarize the core legal dispute in 1-2 sentences)

### *Legal Analysis*
- *Arguments by the Petitioner:* (List up to 3 main arguments as concise sentences)
- *Petitioner Argument Strength:* (Assign a score 0-100 based on clarity, legal grounding, and persuasiveness, with a one-sentence justification)
- *Arguments by the Respondent:* (List up to 3 main arguments as concise sentences)
- *Respondent Argument Strength:* (Assign a score 0-100 based on clarity, legal grounding, and persuasiveness, with a one-sentence justification)
- *Key Evidence:* (List up to 3 pieces of evidence—e.g., witness testimony, documents, precedents—as concise sentences)
- *Evidence Impact Score:* (Assign a score 0-100 based on relevance, reliability, and quantity, with a one-sentence justification)
- *Relevant Laws & Precedents:* (Mention important legal principles or prior cases, if applicable)

### *Court Decision*
- *Judgment:* (Summarize the final ruling—e.g., "Petitioner won" or "Respondent prevailed")
- *Reasoning:* (Explain why the court reached this decision in 1-2 sentences)
- *Outcome:* (State "Win" for Petitioner, "Loss" for Petitioner, or "Unknown")
- *Outcome Reasoning:* (Provide a one-sentence explanation of the inferred outcome)
- *Implications:* (Describe how this ruling might affect future cases or legal interpretations in 1-2 sentences)

### *Full Case Text:*
{cleaned_text}

*Instructions:* 
- Ensure clarity, objectivity, and a professional legal tone. 
- Keep each section concise and structured.
- If data is missing or unclear, note it explicitly (e.g., "No clear arguments identified").
- Do not generate external links or references (e.g., JUDIS.NIC.IN); only use the provided case text.
"""
prompt = PromptTemplate(
    input_variables=["court_name", "petitioner", "case_type", "cleaned_text"],
    template=prompt_template
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Prompt Template for User Argument Scoring
user_prompt_template = """
You are a legal analyst evaluating the strength of arguments. Given the following user-provided arguments, assign a strength score (0-100) based on clarity, legal grounding, and persuasiveness.

### User Arguments:
{user_args}

### Instructions:
- If prefixed with "Plaintiff:" or "Defendant:", score each party's arguments separately.
- Otherwise, provide a general score.
- Return scores with a one-sentence justification.

### Output Format:
- **Plaintiff Score**: (Score 0-100 or None, with justification if applicable)
- **Defendant Score**: (Score 0-100 or None, with justification if applicable)
- **General Score**: (Score 0-100 or None, with justification if applicable)
"""
user_prompt = PromptTemplate(input_variables=["user_args"], template=user_prompt_template)
user_chain = LLMChain(prompt=user_prompt, llm=llm)

# Endpoint: Search Cases
@router.get("/search/")
def search_cases(query: str, top_k: int = 5):
    """Search similar cases based on user query and return row index instead of case_id."""
    try:
        query_embedding = model.encode([query], convert_to_tensor=True).cpu().numpy()
        distances, indices = index.search(query_embedding, top_k)

        retrieved_cases = []
        for i in range(len(indices[0])):
            case_idx = int(indices[0][i])
            case_details = df.iloc[case_idx]
            retrieved_cases.append({
                "index": case_idx,
                "court_name": case_details.get("court_name", "Unknown Court"),
                "petitioner": case_details.get("petitioner", "Unknown"),
                "case_type": case_details.get("case_type", "General"),
                "citations": case_details.get("citations", "None"),
            })

        return {"cases": retrieved_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

# Enhanced Endpoint: Case Details
@router.get("/case_details/")
def get_case_details(index: int):
    """Retrieve detailed case breakdown including arguments, evidence, scores, and outcome."""
    if index < 0 or index >= len(df):
        raise HTTPException(status_code=404, detail=f"Case with index {index} not found.")

    case_details = df.iloc[index].to_dict()
    cleaned_text = " ".join(str(case_details.get('full_case_text', '')).split()[:500])

    try:
        response = llm_chain.run({
            "court_name": case_details.get("court_name", "Unknown Court"),
            "petitioner": case_details.get("petitioner", "Unknown"),
            "case_type": case_details.get("case_type", "General"),
            "cleaned_text": cleaned_text
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating case breakdown: {str(e)}")

    return {
        "index": int(index),
        "court_name": case_details.get("court_name", "Unknown Court"),
        "petitioner": case_details.get("petitioner", "Unknown"),
        "breakdown": response
    }

# Endpoint: Score User Arguments
@router.post("/score_arguments/")
def score_user_arguments(arguments: dict):
    """Score the strength of user-provided arguments."""
    user_input = arguments.get("arguments", "")
    if not user_input:
        raise HTTPException(status_code=400, detail="No arguments provided.")

    try:
        response = user_chain.run({"user_args": user_input})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scoring arguments: {str(e)}")

    # Parse the response
    plaintiff_score = None
    defendant_score = None
    general_score = None
    lines = response.split("\n")
    for line in lines:
        if "Plaintiff Score" in line:
            score = re.search(r"\d+", line)
            plaintiff_score = float(score.group()) if score else None
        elif "Defendant Score" in line:
            score = re.search(r"\d+", line)
            defendant_score = float(score.group()) if score else None
        elif "General Score" in line:
            score = re.search(r"\d+", line)
            general_score = float(score.group()) if score else None

    return {
        "plaintiff_score": plaintiff_score,
        "defendant_score": defendant_score,
        "general_score": general_score,
        "details": response
    }