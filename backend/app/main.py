from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv; import os
from app.routers import recommendations, analytics
load_dotenv()
app = FastAPI(title="AI-ML Product Recommendation API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])
app.include_router(recommendations.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
@app.get("/health")
def health(): return {"status":"ok"}
