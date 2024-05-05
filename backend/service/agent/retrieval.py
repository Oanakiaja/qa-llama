
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Retriever:
    path = './db_data'

    def __init__(self,  embeddingModel="llama3") -> None:
        self.embedding_model = embeddingModel
        self.embeddings = self.__embeddings()
        self.vector_store = Chroma(persist_directory=self.path,
                                   embedding_function=self.embeddings)

        print('retrieval done')

    def load_doc(self, doc_sources=[]):
        docs = self.__load(doc_sources)
        chunks = self.__splits_chunks(docs)
        self.vector_store = self.__vector_store_load(chunks)
        print('load success')

    def __load(self, doc_sources=[]):
        """Indexing: load"""
        print('load data')
        bs4_strainer = bs4.SoupStrainer(
            class_=("post-title", "post-header", "post-content"))
        loader = WebBaseLoader(
            web_paths=doc_sources,
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = loader.load()
        return docs

    def __splits_chunks(self, docs):
        """Indexing: split """
        print('load data: split chunk')
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        chunks = text_splitter.split_documents(docs)
        return chunks

    def __embeddings(self):
        print('embeddings')
        return OllamaEmbeddings(model=self.embedding_model)

    def __vector_store_load(self, chunks):
        print('__vector_store_load')
        return Chroma.from_documents(documents=chunks, embedding=self.embeddings,
                                     persist_directory=self.path
                                     )

    def as_retriever(self, search_type="similarity", search_kwargs={"k": 6}):
        print('as as_retriever')
        return self.vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
