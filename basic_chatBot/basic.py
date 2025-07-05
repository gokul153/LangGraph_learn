from pydantic import BaseModel, Field, HttpUrl
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
from typing import Annotated, List, TypedDict, Union
from langgraph.graph import add_messages
from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage


groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192")
class BasiccChatState(TypedDict):
    """
    State for the basic chat bot.
    """
    messages: Annotated[list,add_messages]

def chatbotnode(state: BasiccChatState):
    return {
        "messages":[llm.invoke(state["messages"])]
    }    

graph = StateGraph(BasiccChatState)
graph.add_node("chatbotnode", chatbotnode)
graph.set_entry_point('chatbotnode')
graph.add_edge("chatbotnode",END)

app = graph.compile()

while True:
    user_input =input("User = ")
    if(user_input in ["exit","end"]):
        break
    else:
        result = app.invoke({
            "messages":[HumanMessage(content=user_input)]
        })
        print(result)