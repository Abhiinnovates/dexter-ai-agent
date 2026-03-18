# graph_pipeline.py
from typing import TypedDict, List, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from web_tools import get_live_indian_ipos, search_financial_news
from parallel_agents import run_parallel_research

# Import your custom agent tools
from company_extractor import extract_companies
from ticker_resolver import resolve_tickers
from parallel_agents import run_parallel_research
from synthesis_agent import synthesize_research


# Define the shared state that agents will pass around
class ResearchState(TypedDict):
    question: str
    tickers: List[str]
    # We use Annotated and operator.add so new research appends to the list instead of overwriting
    research_data: Annotated[List[dict], operator.add]
    report: str
    revision_count: int
    needs_more_research: bool


# graph_pipeline.py (continued)


def extract_node(state: dict):
    print("--- EXTRACTING COMPANIES & TICKERS ---")

    latest_question = state.get("question", "")

    # 1. Get Company Names
    from company_extractor import extract_companies

    companies = extract_companies(latest_question)

    # 2. Get Ticker Symbols
    from ticker_resolver import resolve_tickers

    tickers = resolve_tickers(companies)

    print(f"Found Companies: {companies} | Tickers: {tickers}")

    # 3. Pass EVERYTHING to the next step
    return {
        "companies": companies,
        "tickers": tickers,  # <--- Now research_node won't crash!
        "research_data": [],
    }


def research_node(state: ResearchState):
    tickers = state["tickers"]
    question = state["question"].lower()
    new_data = []

    if "ipo" in question:
        from web_tools import get_live_indian_ipos

        ipo_data = get_live_indian_ipos()
        new_data.append({"Live_Indian_IPOs": ipo_data})

    for ticker in tickers:
        # UPDATE: Pass the state["question"] into the research run
        data = run_parallel_research(ticker, state["question"])
        new_data.append({ticker: data})

    if not tickers and "ipo" not in question:
        from web_tools import search_financial_news

        general_news = search_financial_news(state["question"])
        new_data.append({"General_Market_Search": general_news})

    return {"research_data": new_data}


def synthesize_node(state: dict):
    print("--- SYNTHESIZING REPORT ---")

    # Grab the full history and the newly gathered data
    history = state.get("chat_history", state.get("question", ""))
    data = state.get("research_data", {})

    # Pass them both to your Groq report writer
    from synthesis_agent import synthesize_research

    final_report = synthesize_research(history, data)

    return {"report": final_report}


def critic_node(state: ResearchState):
    revisions = state.get("revision_count", 0)

    # Safely grab the report. If it's None, force it to be an empty string.
    report_text = state.get("report") or ""

    if revisions < 1:
        # Now len() will always be checking a string, even if it's empty
        if len(report_text) < 500:
            return {"needs_more_research": True, "revision_count": revisions + 1}

    return {"needs_more_research": False}


# graph_pipeline.py (continued)


def route_research(state: ResearchState):
    """Conditional edge router."""
    if state["needs_more_research"]:
        return "research_node"
    return "end"


# Build the Graph
workflow = StateGraph(ResearchState)

# Add Nodes
workflow.add_node("extract_node", extract_node)
workflow.add_node("research_node", research_node)
workflow.add_node("synthesize_node", synthesize_node)
workflow.add_node("critic_node", critic_node)

# Add Edges (The Flow)
workflow.set_entry_point("extract_node")
workflow.add_edge("extract_node", "research_node")
workflow.add_edge("research_node", "synthesize_node")
workflow.add_edge("synthesize_node", "critic_node")

# Add Conditional Loop
workflow.add_conditional_edges(
    "critic_node",
    route_research,
    {
        "research_node": "research_node",  # Loop back to research
        "end": END,  # Finish execution
    },
)
# Initialize the memory saver
memory = MemorySaver()

# Compile the graph into a runnable application
research_app = workflow.compile(checkpointer=memory)
