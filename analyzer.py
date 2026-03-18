import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secret key from the .env file instead of hardcoding it!
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "CRITICAL: GROQ_API_KEY is missing. Please set it in your .env file."
    )

# 2. Initialize the client securely
client = Groq(api_key=groq_api_key)


def analyze_data(question, research_data):

    prompt = f"""
    You are a financial analyst AI.

    Research Question:
    {question}

    Data:
    {research_data}

    Provide a financial analysis of the company's revenue growth.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
