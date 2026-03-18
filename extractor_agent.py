import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the environment variables from the .env file
load_dotenv()

# 2. Pull the key securely from the environment
# The Groq library will actually look for os.environ.get("GROQ_API_KEY") automatically,
# but writing it out explicitly is good practice for beginners!
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
from groq import Groq

client = Groq(api_key="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")


def extract_information(question, article):

    prompt = f"""
    Extract important information from this article.

    Research Question:
    {question}

    Article Content:
    {article}

    Return key insights.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
