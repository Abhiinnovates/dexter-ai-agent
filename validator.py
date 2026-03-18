from groq import Groq

# 1. Load the secret key from the .env file instead of hardcoding it!
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "CRITICAL: GROQ_API_KEY is missing. Please set it in your .env file."


def validate_research(question, data):

    prompt = f"""
    You are a financial research validator.

    Question:
    {question}

    Current data:
    {data}

    Decide if the research is sufficient.

    Answer ONLY:
    SUFFICIENT
    or
    NEED_MORE_DATA
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
