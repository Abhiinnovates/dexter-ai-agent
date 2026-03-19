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

def synthesize_research(state: dict):
    # 2. THE ACTUAL FUNCTION (Runs only when the data is ready)
    print("--- SYNTHESIZING REPORT ---")
    
    # Extract data from LangGraph state safely
    question = state.get("question", "")
    research_data = state.get("research_data", [])
    
    today = datetime.now().strftime("%B %d, %Y")

    # Clean the data using your custom function before giving it to the LLM
    llm_safe_data = clean_data_for_llm(research_data)
    compressed_data_string = json.dumps(llm_safe_data, default=str, indent=2)

    prompt = f"""
    You are an elite, Wall Street quantitative financial analyst and AI research agent. 
    Today's date is {today}.

    CRITICAL RULES - READ CAREFULLY:
    1. You are analyzing data for one or more companies.
    2. You MUST write EXACTLY ONE unified report. 
    3. DO NOT write a separate report for each company. Compare them side-by-side UNDER EACH HEADER of the single template.
    4. You MUST use the exact template below exactly ONCE. If you print "### 🏢 1. Company Overview" more than once, you fail your instructions.

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
    
    Write the SINGLE comprehensive report now:
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict Wall Street analyst. You must output exactly ONE report. You are strictly forbidden from repeating the template.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3, 
        )
        
        # 1. Get the raw text from the AI
        raw_report = response.choices[0].message.content
        
        # 2. THE GUILLOTINE: If it printed the header more than once, chop it!
        header = "### 🏢 1. Company Overview & History"
        if raw_report.count(header) > 1:
            print("AI tried to print twice! Chopping the duplicate...")
            # Split the text at the header, keep the first real section, and put the header back on top
            chunks = raw_report.split(header)
            final_report = header + chunks[1]
        else:
            final_report = raw_report

        # 3. Return the perfectly cleaned single report
        return {"report": final_report}

    except Exception as e:
        print(f"Error in synthesis: {e}")
        return {"report": f"Error generating report with Groq: {str(e)}"}
