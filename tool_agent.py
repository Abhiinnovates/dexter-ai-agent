from groq import Groq
from tool_registry import TOOLS

client = Groq(api_key="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")


def choose_tool(question):

    prompt = f"""
    You are an AI agent that chooses tools.

    Available tools:
    - get_revenue: retrieves company revenue data
    - get_stock_info: retrieves company information

    Question:
    {question}

    Return only the tool name.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}]
    )

    tool_name = response.choices[0].message.content.strip()

    return tool_name


def execute_tool(tool_name, ticker):

    if tool_name in TOOLS:

        tool = TOOLS[tool_name]

        return tool(ticker)

    return "Tool not found"
