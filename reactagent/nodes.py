from dotenv import load_dotenv

from agent_reason_runnable import react_agent_runnable, tools
from react_state import AgentState

load_dotenv()

def reason_node(state: AgentState):
     result = react_agent_runnable.invoke({
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"]
    })

    # ✅ Return full state with result
     return {
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"],
        "agent_outcome": result
    }


def act_node(state: AgentState):
    agent_action = state["agent_outcome"]
    
    # Extract tool name and input from AgentAction
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Find the matching tool function
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool with the input
    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"
    
     # ✅ Append to previous steps to avoid overwriting!
    return {
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"] + [(agent_action, str(output))],
        "agent_outcome": None
    }