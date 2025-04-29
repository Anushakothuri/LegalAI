from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import router as search_router  
from prediction import router as prediction_router

app = FastAPI()

# Add CORS middleware (for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routers
app.include_router(search_router)
app.include_router(prediction_router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}