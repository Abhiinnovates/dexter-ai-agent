from groq import Groq

client = Groq(api_key="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")


def create_plan(question):

    prompt = f"""
    You are a financial research planner.

    Break the following question into clear steps.

    Question:
    {question}

    Return numbered steps.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
