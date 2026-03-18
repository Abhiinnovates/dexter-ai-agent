import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

# Initialize the Groq Client
client = Groq(api_key=groq_api_key)


def resolve_tickers(companies: list) -> list:
    """
    Takes a list of company names and returns their stock ticker symbols using Groq.
    """
    if not companies:
        return []

    prompt = f"""
    Convert these company names into their official US stock ticker symbols: {companies}. 
    Return ONLY a comma-separated list of tickers (e.g. AAPL, TSLA, AMZN). 
    Do not include any other text, explanation, or the company names.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        result = response.choices[0].message.content
        if result:
            return [ticker.strip().upper() for ticker in result.split(",")]
        return []

    except Exception as e:
        print(f"Ticker Resolution Error: {e}")
        return []
