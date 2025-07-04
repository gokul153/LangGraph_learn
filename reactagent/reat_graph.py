from dotenv import load_dotenv

load_dotenv()

from langchain_core.agents import AgentFinish, AgentAction
from langgraph.graph import END, StateGraph

from nodes import reason_node, act_node
from react_state import AgentState

REASON_NODE = "reason_node"
ACT_NODE = "act_node"
# ✅ Add max step tracking
MAX_STEPS = 8

def should_continue(state: AgentState) -> str:
     # ✅ Terminate if max steps exceeded (safety)
   
    if isinstance(state["agent_outcome"], AgentFinish):
        print( state["agent_outcome"])
        print("🛑 Agent finished. Halting.")
        return END
    elif len(state["intermediate_steps"]) >= MAX_STEPS:
        print("🛑 Max steps exceeded. Halting to avoid infinite loop.")
        return END
    else:
        return ACT_NODE


graph = StateGraph(AgentState)

graph.add_node(REASON_NODE, reason_node)
graph.set_entry_point(REASON_NODE)
graph.add_node(ACT_NODE, act_node)


graph.add_conditional_edges(
    REASON_NODE,
    should_continue,
)

graph.add_edge(ACT_NODE, REASON_NODE)

app = graph.compile()

result = app.invoke(
    {
        "input": "When did the last airplane crash happen in india and how many days from the current date was the accident ?", 
        "agent_outcome": None, 
        "intermediate_steps": []
    }
)
print(result)
print("////////////////////////")

print(result["agent_outcome"].return_values["output"], "final result")