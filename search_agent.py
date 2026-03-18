from duckduckgo_search import DDGS


def search_web(query):

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(query, max_results=5)

        for r in search_results:

            results.append({"title": r["title"], "url": r["href"]})

    return results
