from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from urllib3 import response

from ai_engine import OPENAI_API_KEY, generate_tutoring_response, generate_quiz

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="AI Tutor API",
    description="API for generating personalized tutoring content and quizzes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #for development - restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class TutorRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Learning level (Beginner, Intermediate, Advanced)")
    question: str = Field(..., description="User's question")
    learning_style: str = Field("Text-based", description="Preferred learning style")
    background: str = Field("Unknown", description="Background knowledge level")
    language: str = Field("English", description="Preferred language")


class QuizRequest(BaseModel):
    subject: str = Field(..., description="Academic subject")
    level: str = Field(..., description="Learning level")
    num_questions: int = Field(5, description="Number of quiz questions", ge=1, le=10)
    reveal_format: Optional[bool] = Field(True, description="Whether to format with hidden answers")


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class TutorResponse(BaseModel):
    response: str

class QuizResponse(BaseModel):
    quiz: List[Dict[str, Any]]
    formatted_quiz: Optional[str] = None


@app.post("/tutor", response_model=TutorResponse)
async def handle_tutoring_request(data: TutorRequest):
    """
     Generate a personalized tutoring explanation based on user preferences.
    """
    try:
        explanation = generate_tutoring_response(
            data.subject,
            data.level,
            data.question,
            data.learning_style,
            data.background,
            data.language
        )
        return {"response": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")


@app.post("/quiz", response_model=QuizResponse)
async def generate_quiz_api(data: QuizRequest):
    """
     Generate a quiz with multiple-choice questions based on subject and level.
    """
    try:
        quiz_result = generate_quiz(
            data.subject,
            data.level,
            data.num_questions,
            reveal_answer=data.reveal_format
        )
        # The generate_quiz function now returns the correct format directly
        return quiz_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@app.get("/quiz-html/{subject}/{level}/{num_questions}", response_class=HTMLResponse)
async def generate_quiz_html(subject: str, level: str, num_questions: int = 5):
    """ 
    Get a formatted HTML quiz page.
    """
    try:
        quiz_result = generate_quiz(subject, level, num_questions, reveal_answer=True)
        return quiz_result["formatted_quiz"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz HTML: {str(e)}")




@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """

    return {"status": "healthy"}