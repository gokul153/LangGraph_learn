from typing import List
from langchain_core.messages import BaseMessage , ToolMessage
from langgraph.graph import END , MessageGraph
from correctionChain import revisor_chain , reponder_chain
from execute_tools import execute_tools
MAX_ITERATION = 2
graph = MessageGraph()
graph.add_node("draft",reponder_chain)
graph.add_node("execute_tools",execute_tools)
graph.add_node("revisor",revisor_chain)

graph.add_edge("draft","execute_tools")
graph.add_edge("execute_tools","revisor")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item,ToolMessage) for item in state)
    num_iteration = count_tool_visits
    if num_iteration>MAX_ITERATION:
        return END
    return "execute_tools"

graph.add_conditonal_edges("revisor",event_loop)
graph.set_entry_point("draft")
app = graph.compile
print(app.get_graph().draw_mermaid())

response = app.invoke(
    "Write about how small message can leverage AI to grow"
)
print(response)
print("\n////")
