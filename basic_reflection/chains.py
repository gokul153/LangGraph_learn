from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
#from langchain_core.messages import BaseMessage , HumanMessage
from langchain.schema import BaseMessage, HumanMessage

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a twitter techie influencer assistant tasked with writing excellent twitter posts.
Generate the best twitter post possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempts."""),
        MessagesPlaceholder(variable_name="messages") 
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet . Generate critique and recommendation for the users tweet."
            "Always provide detailed recommendations, including requests for length virality"
        ),
         MessagesPlaceholder(variable_name="messages") 
    ]
)

groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-8b-8192")

generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm