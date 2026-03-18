import yfinance as yf
import pandas as pd


def get_revenue(ticker):

    stock = yf.Ticker(ticker)

    financials = stock.financials

    if financials.empty:
        return "No financial data available"

    # possible revenue labels
    revenue_labels = ["Total Revenue", "Revenue", "Operating Revenue"]

    for label in revenue_labels:

        if label in financials.index:

            return financials.loc[label]

    return "Revenue data not found"


def get_stock_info(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
    }


def get_revenue(ticker):
    # ... [Keep your existing get_revenue code exactly as it is] ...
    pass


def get_historical_prices(ticker, question):
    """Fetches historical prices dynamically based on the user's timeframe."""
    q = question.lower()

    # Smart Timeframe Extraction
    period = "6mo"  # Default fallback
    if "1 month" in q or "30 day" in q:
        period = "1mo"
    elif "3 month" in q or "90 day" in q:
        period = "3mo"
    elif "6 month" in q:
        period = "6mo"
    elif "1 year" in q or "12 month" in q:
        period = "1y"
    elif "2 year" in q or "24 month" in q:
        period = "2y"
    elif "5 year" in q:
        period = "5y"
    elif "max" in q or "all time" in q:
        period = "max"

    print(f"📈 Fetching {period} price history for {ticker}...")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": f"No historical data found for {ticker}."}

        hist = hist.reset_index()
        hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")
        price_data = hist[["Date", "Close"]].to_dict(orient="records")

        return {"ticker": ticker, "timeframe": period, "historical_prices": price_data}
    except Exception as e:
        return {"error": str(e)}


def get_fundamentals(ticker):
    """Fetches deep fundamental data, ratios, and corporate info."""
    print(f"📊 Fetching deep fundamentals for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract all the critical data points you requested
        fundamentals = {
            "Market Cap": info.get("marketCap", "N/A"),
            "Trailing P/E": info.get("trailingPE", "N/A"),
            "Forward P/E": info.get("forwardPE", "N/A"),
            "EPS (Trailing)": info.get("trailingEps", "N/A"),
            "Live Volume": info.get("volume", "N/A"),
            "Average Volume (10 day)": info.get("averageVolume10days", "N/A"),
            "Total Assets": info.get("totalAssets", "N/A"),
            "Total Debt": info.get("totalDebt", "N/A"),
            "Revenue Growth": info.get("revenueGrowth", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "Business Summary": info.get("longBusinessSummary", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            # Grab the top 3 executives
            "Top Management": [
                officer.get("name") for officer in info.get("companyOfficers", [])[:3]
            ],
        }

        return {"ticker": ticker, "fundamentals": fundamentals}

    except Exception as e:
        print(f"❌ Failed to fetch fundamentals for {ticker}: {e}")
        return {"error": f"Fundamentals not found: {str(e)}"}
    import requests


import os
from dotenv import load_dotenv

load_dotenv()


def get_fmp_fundamentals(ticker: str) -> dict:
    """
    Fetches the latest annual income statement using Financial Modeling Prep (FMP).
    """
    fmp_api_key = os.environ.get("FMP_API_KEY")

    if not fmp_api_key:
        return {"error": "FMP_API_KEY is missing from environment variables."}

    # FMP API Endpoint for the Income Statement
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=3&apikey={fmp_api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if not data:
            return {"error": f"No fundamental data found for {ticker}."}

        # Extract the last 3 years of revenue and net income to give the LLM context
        financial_summary = {"ticker": ticker, "annual_data": []}

        for year in data:
            financial_summary["annual_data"].append(
                {
                    "date": year.get("date"),
                    "revenue": year.get("revenue"),
                    "net_income": year.get("netIncome"),
                    "eps": year.get("eps"),
                }
            )

        return financial_summary

    except requests.exceptions.RequestException as e:
        return {"error": f"FMP API request failed: {str(e)}"}
