import pandas as pd
import requests
from duckduckgo_search import DDGS
from datetime import datetime


def search_financial_news(query):
    """Searches for general financial news based on a query."""
    results = []
    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=5)
            for r in search_results:
                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "body": r.get("body", ""),
                    }
                )
    except Exception as e:
        print(f"❌ News search failed: {e}")
        return [{"error": "Failed to fetch news."}]

    return results


def get_live_indian_ipos():
    """Directly scrapes structured live Mainboard and SME IPO tables using Pandas."""
    print("🕵️ Agent is extracting live IPO tables directly from the web...")

    # We target a reliable IPO tracker that uses clean HTML tables
    url = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"

    # Websites block bots, so we must disguise our scraper as a standard web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        # pandas.read_html is magic: it finds all <table> tags and converts them to DataFrames!
        tables = pd.read_html(response.text)

        if tables:
            # The first table usually contains the live Mainboard and SME IPOs
            df = tables[0]

            # Convert the DataFrame into a JSON-like dictionary list so the LLM can read it perfectly
            ipo_list = df.to_dict(orient="records")

            print(
                f"✅ Successfully extracted a table with {len(ipo_list)} IPO entries."
            )
            return ipo_list

    except Exception as e:
        print(f"❌ Table extraction failed: {e}")
        return [{"error": f"Failed to scrape IPO tables: {str(e)}"}]

    return [{"message": "No tables found on the IPO tracking site."}]

    print(f"✅ Found {len(results)} search results for IPOs.")
    return results
