from typing import List
from service.agent.utils import escape_str
from service.agent.invoke import QAAnswer, invoke_llama3, astream_invoke_llama3
from service.agent.chain import retrieval_client
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document

load_dotenv()

# fastapi
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "llama3"}


class QaReqBody(BaseModel):
    session: str
    question: str = None


@app.post("/stream/qa", response_model=QAAnswer)
async def invoke(bodyModel: QaReqBody):
    body = bodyModel.model_dump()
    session = body['session']
    question = body['question']
    return invoke_llama3(session, question)


@app.post("/astream/qa")
async def invoke_streaming(bodyModel: QaReqBody):
    body = bodyModel.model_dump()
    session = body['session']
    question = body['question']

    print('start chain')

    astream = astream_invoke_llama3(session, question)

    async def event_generator():
        # {'input': 'xx'}
        # {'chat_history': []}
        # {'context: [Document(page_content:str, metadata{source: str})]}
        # {'answer': 'xxx'}
        async for chunk in astream:
            if 'context' in chunk:
                documents: List[Document] = chunk.get('context')
                msg = 'event:references\ndata:[{docs}]\n\n'
                docs = ""

                for doc in documents:
                    source = escape_str(doc.metadata.get("source"))
                    content = escape_str(doc.page_content)
                    if source == None or content == None:
                        continue;
                    docs += "{" + f'"source": {source}, "content": {content}' + "},"
                docs = docs[:-1]
                yield msg.replace("{docs}", docs)

            elif 'answer' in chunk:
                answer = chunk.get('answer')
                yield f'event:content\ndata:{answer}\n\n'

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class LoadRepoReqBody(BaseModel):
    repo: str


@app.post("/stream/load_doc")
async def load_doc(bodyModel: LoadRepoReqBody):
    body = bodyModel.model_dump()
    repo = body['repo']
    retrieval_client.load_doc([repo])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
