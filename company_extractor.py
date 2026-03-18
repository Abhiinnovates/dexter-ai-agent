import os
from groq import Groq
from dotenv import load_dotenv

# 1. SETUP: Load environment variables
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "CRITICAL: GROQ_API_KEY is missing. Please set it in your .env file."
    )

# Initialize the Groq Client
client = Groq(api_key=groq_api_key)


def extract_companies(user_query: str) -> list:
    """
    Extracts company names from the user's financial question using Groq.
    """
    prompt = f"""
    Extract the company names mentioned in this query. 
    Return ONLY a comma-separated list of company names. If none, return 'None'.
    Query: "{user_query}"
    """

    try:
        # 2. CALL GROQ
        # We use llama-3.3-70b-versatile, though llama3-8b-8192 is also incredibly fast for simple extraction!
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise financial data extraction assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,  # Low temperature so it doesn't hallucinate extra companies
        )

        # 3. PARSE THE RESPONSE
        result = response.choices[0].message.content

        if result and result.strip().lower() != "none":
            # Clean up the output, split by comma, and return as a Python list
            return [company.strip() for company in result.split(",")]

        return []

    except Exception as e:
        print(f"Groq Extraction Error: {e}")
        return []


# Quick test block (Runs only if you execute this file directly)
if __name__ == "__main__":
    test_query = "What is the revenue growth and market outlook for Tesla and Apple?"
    print(f"Testing extraction on: '{test_query}'")
    print(f"Extracted: {extract_companies(test_query)}")
