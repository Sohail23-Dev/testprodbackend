from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List

# Create FastAPI instance
app = FastAPI(
    title="User Details API",
    description="Backend API for fetching user details",
    version="1.0.0"
)

# Get allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Define response model
class UserDetails(BaseModel):
    name: str
    age: int
    sex: str

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "user-details-api"}

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "User Details API is running!",
        "version": "1.0.0",
        "endpoints": ["/health", "/user-details"]
    }

# User details endpoint
@app.get("/user-details", response_model=UserDetails)
def get_user_details():
    # For production, you might want to fetch this from a database
    # or from environment variables for testing
    return {
        "name": os.getenv("TEST_USER_NAME", "Sohail"),
        "age": int(os.getenv("TEST_USER_AGE", "25")),
        "sex": os.getenv("TEST_USER_SEX", "Male")
    }