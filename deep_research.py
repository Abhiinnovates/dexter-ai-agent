from search_agent import search_web
from web_reader import read_article
from extractor_agent import extract_information
from research_memory import memory


def deep_research(question):

    search_results = search_web(question)

    for result in search_results:

        article = read_article(result["url"])

        insight = extract_information(question, article["text"])

        memory.add(insight, result["url"])

    return memory.get_all()
