from langchain_community.chat_models import ChatOllama


class ChatModel:
    def ollama(cls, model='llama3') -> ChatOllama:
        return ChatOllama(model=model)
