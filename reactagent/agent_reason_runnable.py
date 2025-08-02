
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_tavily import TavilySearch

from langchain.agents import initialize_agent, AgentType, tool,create_react_agent
import datetime
from langchain_groq import ChatGroq



from langchain import hub
search_tool = TavilySearch(
    search_depth="basic"
   
)
groq_api_key=os.getenv("GROQ_API_KEY")
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time


react_prompt = hub.pull("hwchase17/react")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="mistral-saba-24b",  # other options: mixtral-8x7b, llama3-8b, etc.
    streaming=True
)
# llm = ChatAnthropic(
#     model="claude-3-opus-20240229",  # You can also use claude-3-sonnet-20240229 or claude-3-haiku-20240307
#     temperature=0.7,
#     streaming=True
# )
tools = [search_tool,get_system_time]
react_prompt = hub.pull("hwchase17/react")
react_agent_runnable = create_react_agent(tools=[search_tool,get_system_time],
                   llm=llm,prompt=react_prompt)

