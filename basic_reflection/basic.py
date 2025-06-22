from typing import List, Sequence
from dotenv import load_dotenv
#from langchain_core.message import BaseMessage, HumanMessage
from langchain.schema import BaseMessage, HumanMessage

from langgraph.graph import END, MessageGraph

from chains import generation_chain , reflection_chain

load_dotenv()

graph = MessageGraph()

REFLECT = "reflect"
GENERATE ="generate"

def generate_node(state):
    return generation_chain.invoke({
        "messages":state
    })

def reflect_node(state):
    response = reflection_chain.invoke({
        "messages":state
    })
    return [HumanMessage(content = response.content)]

graph.add_node(GENERATE,generate_node)
graph.add_node(REFLECT,reflect_node)

graph.set_entry_point(GENERATE)

def should_continue(state):
    print("Current length of state:", len(state))
    print("Current state content:", state)
    if(len(state) > 5):
        return END
    return REFLECT

## after the genrate node is executed it should go to should_continue
# graph.add_conditional_edges(GENERATE,should_continue)
graph.add_conditional_edges(GENERATE, should_continue,
                            {
                                REFLECT:REFLECT,
                                END:END
                            })


graph.add_edge(REFLECT,GENERATE)
app = graph.compile()
print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()   

response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))

print(response)