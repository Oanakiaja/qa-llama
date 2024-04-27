# LangChain supports many other chat models. Here, we're using Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# from langchain_community.document_loaders import WebBaseLoader


from typing import Union

prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

llm = ChatOllama(model="llama3")

chain = prompt | llm | StrOutputParser()

# print(chain.invoke({"topic": "Space travel"}))


def invoke_llama3(str: Union[str, None] = None):
    if (str is None):
        return chain.invoke({"topic": "llama"})
    return chain.invoke({"topic": str})
