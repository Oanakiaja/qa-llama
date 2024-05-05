
from typing import AsyncIterator, List, Union
from pydantic import BaseModel
from .chain import conversational_rag_chain
from langchain_core.documents import Document


class QAAnswer(BaseModel):
    answer: str
    # context: List[Document]

# page_content=
    #    'The AI assistant can parse user input to several tasks: [{"task": task, "id", task_id, "dep": dependency_task_ids, "args": {"text": text, "image": URL, "audio": URL, "video": URL}}]. The "dep" field denotes the id of the previous task which generates a new resource that the current task relies on. A special tag "-task_id" refers to the generated text image, audio and video in the dependency task with id as task_id. The task MUST be selected from the following options: {{ Available Task List }}. There is a logical relationship between tasks, please note their order. If the user input can\'t be parsed, you need to reply empty JSON. Here are several cases for your reference: {{ Demonstrations }}. The chat history is recorded as {{ Chat History }}. From this chat history, you can find the path of the user-mentioned resources for your task planning.',
    #    metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent', 'start_index': 17804})


def invoke_llama3(session: str, question: Union[str, None] = None) -> str:
    chain_output = conversational_rag_chain.invoke(
        {"input": question},
        config={
            "configurable": {"session_id": session}
        },
    )
    answer = chain_output['answer']
    return QAAnswer(answer=answer)


def astream_invoke_llama3(session: str, question: Union[str, None] = None) -> AsyncIterator:
    return conversational_rag_chain.astream(
        {"input": question},
        config={
            "configurable": {"session_id": session}
        },
    )
