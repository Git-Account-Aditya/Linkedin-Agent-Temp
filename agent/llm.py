import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def llm():
    apikey = os.getenv("GROQ_API_KEY")
    if not apikey:
        raise ValueError("GROQ_API_KEY environment variable is not set.")  
    
    groq = ChatGroq(api_key=apikey,
                    model='llama-3.3-70b-versatile')
    return groq

