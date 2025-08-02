import operator
from typing import Annotated, List, TypedDict, Union
from langchain_core.agents import AgentAction, AgentFinish

class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish,None]
    intermediate_steps: Annotated[List[tuple[AgentAction,str]],operator.add]
