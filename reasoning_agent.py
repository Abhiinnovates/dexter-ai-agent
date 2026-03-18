from groq import Groq

client = Groq(api_key="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")


def decide_next_action(question, memory):

    prompt = f"""
    You are an autonomous research agent.

    Question:
    {question}

    Current knowledge:
    {memory}

    Decide what to do next.

    Options:
    - get_revenue
    - get_stock_info
    - finish

    Return only one option.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
