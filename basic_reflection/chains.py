from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage

generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a twitter techie influencer assistant tasked with writing excellent twitter posts.
Generate the best twitter post possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempts."""),
        MessagesPlaceholder(variable_name="chat_history"), # Add back for conversational memory
        ("human", "{question}"),
    ]
)
