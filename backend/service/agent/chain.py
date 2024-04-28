from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains import create_retrieval_chain

from .prompt import qa_prompt, contextualize_q_prompt
from .retrieval import Retriever
from .llm import ChatModel


retriever = Retriever(
    doc_sources=["https://lilianweng.github.io/posts/2023-06-23-agent"],
    embeddingModel="llama3").as_retriever()
llm = ChatModel.ollama('llama3')

# Create history-aware retriever chain
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Create q&a chain to process retrieved documents
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Chain the history-aware retriever and QA chains
rag_chain = create_retrieval_chain(
    history_aware_retriever, question_answer_chain)


#  manage chat history -> TODO: redis or sql
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# conversational
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)
