
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from typing import Union
from langchain_core.output_parsers import StrOutputParser

# llm
from langchain_community.chat_models import ChatOllama
llm = ChatOllama(model="llama3")


# Retrieval

# Indexing: load
bs4_strainer = bs4.SoupStrainer(
    class_=("post-title", "post-header", "post-content"))
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs={"parse_only": bs4_strainer},
)
docs = loader.load()
# print(f"Loaded {len(docs)} documents: {docs}")

# Indexing: split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

# print(f"Loaded {len(all_splits)} documents: {all_splits}")


# Indexing: store

embeddings = OllamaEmbeddings(model="llama3")
vector_store = Chroma.from_documents(
    documents=all_splits, embedding=embeddings)

# Retrieve
# TODO: MultiQueryRetriever \ MultiVectorRetriever \ Max marginal relevance \ Self-Query Retriever
retriever = vector_store.as_retriever(
    search_type="similarity", search_kwargs={"k": 6})

# LLM Generator

# https://smith.langchain.com/hub/rlm/rag-prompt
# Prompt
# from Remote
# prompt = hub.pull("rlm/rag-prompt")

# HUMAN
# You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
# If you don't know the answer,just say that you don't know. Use three sentences maximum and keep the answer concise.
# Question: {question}
# Context: {context}
# Answer:

# Customized Prompt
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)


def invoke_llama3(str: Union[str, None] = None):
    if (str is None):
        return rag_chain.invoke("What is the article about?")
    return rag_chain.invoke(str)
