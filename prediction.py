import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Define router
router = APIRouter()

# ✅ Correct paths for your trained model
MODEL_DIR = r"C:\legal_ai\backend\models\legal_bert_model\checkpoint-45000"
TOKENIZER_DIR = r"C:\legal_ai\backend\models\legal_bert_model"

# ✅ Load Tokenizer & Model from local directories
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR, device_map="cpu")

# ✅ Set model to evaluation mode
model.eval()

# ✅ Load LLM for Reasoning (Mistral-24B)
llm = ChatGroq(model_name="mistral-saba-24b", temperature=0.3, groq_api_key=GROQ_API_KEY)

# ✅ Define Prompt for Generating Case Outcome Reasoning
reasoning_prompt = PromptTemplate(
    input_variables=["case_text", "predicted_label"],
    template="""
    You are a highly skilled legal analyst. Given the details of a legal case, analyze the factors that contribute to the predicted outcome: "{predicted_label}".
    
    ### Legal Case Details:
    {case_text}

    ### Case Analysis:
    - **Key Arguments for the Plaintiff (Winning Party)**
    - **Key Arguments for the Defendant (Losing Party)**
    - **Relevant Legal Precedents & Laws**
    - **Weaknesses in the Losing Party's Case**
    - **Why this case is likely to be a {predicted_label}**

    Provide a structured, objective, and professional legal reasoning.
    """
)
llm_chain = LLMChain(prompt=reasoning_prompt, llm=llm)

# ✅ Define Legal Case Input Structure
class CaseText(BaseModel):
    text: str

# ✅ Define Class Labels (Win/Loss Prediction)
class_labels = ["Loss", "Win"]

@router.post("/predict/")
async def predict(case: CaseText):
    """
    Predicts whether the case is likely to be won or lost and provides a reasoning.
    """
    # ✅ Tokenize input text
    encoding = tokenizer(case.text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")

    # ✅ Ensure tensors are on CPU
    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    # ✅ Run model inference
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        logits = outputs.logits

    # ✅ Convert logits to probabilities
    probabilities = F.softmax(logits, dim=1).numpy()[0]
    predicted_label_index = probabilities.argmax()
    confidence = probabilities[predicted_label_index]

    # ✅ Validate label index
    if predicted_label_index >= len(class_labels):
        raise HTTPException(status_code=500, detail="Invalid class prediction.")

    predicted_label = class_labels[predicted_label_index]

    # ✅ Generate case-specific reasoning
    reasoning = llm_chain.run({"case_text": case.text, "predicted_label": predicted_label})

    return {
        "predicted_label": predicted_label,  # "Win" or "Loss"
        "confidence": float(confidence),
        "reasoning": reasoning
    }
