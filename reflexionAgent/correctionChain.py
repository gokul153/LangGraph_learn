from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from schema import AnswerQuestion ,ReviseAnswer # Ensure this is a valid Pydantic model
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Load Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")

# Init LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

# Use structured output
structured_llm = llm.with_structured_output(AnswerQuestion)

# Prompt
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert AI assistant. Provide structured answers.

Current time: {time}

1. {first_instruction}
2. Reflect on your answer critically and point out weaknesses.
3. List 1-3 search queries separately for further research.
"""
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
    first_instruction="Write a ~250 word blog post about how small provision stores can leverage AI to grow."
)

# Chain
reponder_chain = prompt_template | structured_llm

# Invoke
response = reponder_chain.invoke({
    "messages": [
        HumanMessage(content="Write a blog post on how small provision stores can leverage AI to grow.")
    ]
})

# Output structured result
print("✅ Responder Output:\n", response)

structured_llm_revisor = llm.with_structured_output(ReviseAnswer)
revise_instructions = """Revise your previous answer using the new information.
- Use the critique to add missing info.
- Include numerical citations in your revised answer.
- Add a "References" section to the bottom of your answer (not part of the 250 word limit) like:
    - [1] https://example.com
    - [2] https://example.com
- Remove superfluous details and ensure the response is still within 250 words.
"""
revisor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI agent that revises prior answers based on user critique.

Current time: {time}

Instructions:
1. {first_instruction}
2. Provide a concise, accurate revision with citations and remove any redundancy.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Return only the revised result using the `ReviseAnswer` format."
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
        first_instruction=revise_instructions
)

revisor_chain = revisor_prompt_template | structured_llm_revisor
revisor_response = revisor_chain.invoke({
    "messages": [HumanMessage("AI Agents taking over content creation")]
})
print("✅ Revisor Output:\n", revisor_response)