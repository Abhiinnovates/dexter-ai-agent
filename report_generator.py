from groq import Groq

client = Groq(api_key="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")


def generate_report(question, research_data):

    formatted_sources = ""

    for r in research_data:

        formatted_sources += f"{r['insight']}\nSource: {r['source']}\n\n"

    prompt = f"""
    Write a research report.

    Question:
    {question}

    Evidence:
    {formatted_sources}

    Include citations for each claim.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
