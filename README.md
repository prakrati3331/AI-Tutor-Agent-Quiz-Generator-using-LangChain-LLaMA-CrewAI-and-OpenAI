# AI Tutor Agent & Quiz Generator

Develop an AI-powered tutor Agent and quiz generator using LangChain, LLaMA, CrewAI, and OpenAI. The system will generate quizzes based on a selected topic, provide detailed topic plans, and offer personalized tutoring using AI models. A user-friendly interface using Streamlit and a backend powered by FastAPI will ensure seamless interaction.


# Topics Covered:

Select topics using Streamlit and analyze with LLaMA or OpenAI.

Generate quizzes using CrewAI with adaptive difficulty.

Provide AI tutor support via GPT for explanations and summaries.

Create study plans with LangChain and recommend resources.

Manage backend using FastAPI and store data with Pinecone.



# use this version for langchain and langchain-community

 langchain==0.3.13
 langchain-core==0.3.28
 langchain-community==0.3.13
 langchain-openai==0.2.14

 
 

# How to run this app:

#uvicorn main:app --reload

#streamlit run app.py

check :current directory is : cd


# steps 
# for creating environment

1. conda create -n lang6 python=3.11 -y   ,  conda activate lang6  or

2. python -m venv venv   ,  .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
