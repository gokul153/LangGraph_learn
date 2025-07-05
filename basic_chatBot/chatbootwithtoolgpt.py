from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

# Load .env for OPENAI_API_KEY
load_dotenv()

# Define the state structure
class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

# Search tool integration
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

# Initialize OpenAI LLM (can be gpt-4 or gpt-3.5-turbo)
llm = ChatOpenAI(model="gpt-4")  # or "gpt-3.5-turbo"

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools=tools)

# Chatbot logic using OpenAI
def chatbot(state: BasicChatBot):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])],
    }

# Conditional routing based on tool_calls
def tools_router(state: BasicChatBot):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_node"
    else:
        return END

# Tool execution node
tool_node = ToolNode(tools=tools)

# Create the LangGraph
graph = StateGraph(BasicChatBot)
graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router, {
    "tool_node": "tool_node",
    END: END
})
graph.add_edge("tool_node", "chatbot")

# Compile the app
app = graph.compile()

# Main loop for interaction
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "end"]:
        break
    result = app.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    print(result["messages"][-1].content)
