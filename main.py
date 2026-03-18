from planner import create_plan
from parallel_agents import run_parallel_research
from synthesis_agent import synthesize_research
from vector_memory import memory

question = "Analyze Tesla revenue growth and market outlook"

ticker = "TSLA"

print("\nUSER QUESTION:\n", question)

plan = create_plan(question)

print("\nRESEARCH PLAN:\n", plan)

research_results = run_parallel_research(ticker)

for r in research_results:
    memory.add(str(r))

relevant_data = memory.search(question)

report = synthesize_research(question, relevant_data)

print("\nFINAL REPORT:\n")

print(report)
