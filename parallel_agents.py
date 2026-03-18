from concurrent.futures import ThreadPoolExecutor
from tools import (
    get_revenue,
    get_historical_prices,
    get_fundamentals,
)  # <-- Import the new tool
from web_tools import search_financial_news


def financial_agent(ticker):
    return f"Revenue Data:\n{get_revenue(ticker)}"


def news_agent(company):
    return f"News:\n{search_financial_news(company)}"


def price_agent(ticker, question):
    return get_historical_prices(ticker, question)


def fundamentals_agent(ticker):  # <-- Create the new worker
    return get_fundamentals(ticker)


def run_parallel_research(ticker, question):
    with ThreadPoolExecutor() as executor:
        # Submit ALL FOUR tasks simultaneously
        f1 = executor.submit(financial_agent, ticker)
        f2 = executor.submit(news_agent, ticker)
        f3 = executor.submit(price_agent, ticker, question)
        f4 = executor.submit(fundamentals_agent, ticker)

        results = [
            f1.result(),
            f2.result(),
            f3.result(),
            f4.result(),  # <-- Add the fundamentals to the final results
        ]

    return results
