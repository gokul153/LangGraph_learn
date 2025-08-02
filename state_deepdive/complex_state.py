
from typing import TypedDict,List, Annotated
from langgraph.graph import StateGraph, END
import operator
class SimpleState(TypedDict):
    """
    A simple state representation using TypedDict.
    """
    count: int
    sum: Annotated[int, operator.add]  # Annotated field for clarity
    history: Annotated[List[int] ,operator.concat]  # Optional field to keep track of history


def increment(state: SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    return{
        "count":new_count
        , "sum": new_count,
        "history": [new_count]  # Append the new count to history
    }

def should_continue(state):
    if(state["count"]<5):
        return "continue"
    else:
        return "stop"
    


graph = StateGraph(SimpleState)    
graph.add_node("increment", increment)
graph.set_entry_point("increment")
graph.add_conditional_edges("increment",  should_continue,{
    "continue" : "increment",
    "stop" : END
})
app = graph.compile()
state = {    "count": 0,
            "sum": 0,
            "history": []  # Initialize history as an empty list
        }
result = app.invoke(state)
print(result)