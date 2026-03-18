import os
import json
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# 1. SETUP (Runs immediately when the app starts)
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "CRITICAL: GROQ_API_KEY is missing. Please set it in your .env file."
    )

# Initialize the Groq Client
client = Groq(api_key=groq_api_key)


def clean_data_for_llm(data):
    """Recursively removes massive arrays to keep the prompt clean and focused."""
    if isinstance(data, dict):
        if "historical_prices" in data:
            return {
                "ticker": data.get("ticker", "Unknown"),
                "note": "Chart data securely passed to UI.",
            }
        return {k: clean_data_for_llm(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data_for_llm(item) for item in data]
    elif isinstance(data, str):
        return data[:1200] + "... [Truncated for limits]" if len(data) > 1200 else data
    else:
        return data


def synthesize_research(question, research_data):
    # 2. THE ACTUAL FUNCTION (Runs only when the data is ready)
    today = datetime.now().strftime("%B %d, %Y")

    llm_safe_data = clean_data_for_llm(research_data)
    compressed_data_string = json.dumps(llm_safe_data, default=str, indent=2)

    prompt = f"""
    You are an elite, Wall Street quantitative financial analyst and AI research agent. 
    Today's date is {today}.

    CRITICAL OUTPUT INSTRUCTIONS:
    You MUST generate a highly detailed, comprehensive investment report. You are strictly required to use the exact template below. Highlight each main point in bold. Do NOT skip any sections. If specific qualitative data is not in the raw data, deduce reasonable assumptions based on the industry news or state that it is undisclosed, but you MUST address the header.

    MANDATORY REPORT TEMPLATE:

    ### 🏢 1. Company Overview & History
    * **Company History & Line of Business:**
    * **Parent Company:** * **Top Management:** ### 📦 2. Products, Market & Intellectual Property
    * **Various Products & Services:**
    * **Product Market Demand & Market Share:**
    * **Patents and Trademarks:**

    ### 📊 3. Deep Fundamentals & Financial Ratios
    * **Current Price:**
    * **Market Cap:**
    * **P/E Ratio & EPS:**
    * **Growth Metrics:**
    * **Assets vs. Liabilities:**
    * **Calculated Financial Ratios:** ### 📈 4. Trading Volume Analysis
    * **Live Volume of Trade:**
    * **Past 7 Days Volume Trend:** ### ⚔️ 5. Competitive Landscape
    * **Direct Competitors:**
    * **Indirect Competitors:**

    ### 🤝 6. Future Outlook & Corporate Moves
    * **Future Business Plans:**
    * **New Contracts, Partnerships, or Top Clients:**

    ### ⚠️ 7. Risk Assessment & Economics
    * **Risk Assessment:**
    * **Macro-Economic Factors:**

    ### 🧠 8. Valuation & Investment Decision
    * **Valuation Method Used:** * **Final Investment Decision:** * **FINAL STOCK SCORE:** [Give a definitive number out of 100 based on fundamentals and momentum]

    Conversation History:
    {question}

    New Compressed Data Gathered from Research Tools:
    {compressed_data_string}
    
    Write the comprehensive report now:
    """

    try:
        # 3. CALL GROQ INSIDE THE FUNCTION
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an elite financial analyst. Write a professional, data-driven report.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        # Return the generated text back to your app
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating report with Groq: {str(e)}"
