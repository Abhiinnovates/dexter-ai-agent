from groq import Groq

client = Groq(api_key="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")


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
