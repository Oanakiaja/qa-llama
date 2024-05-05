from service.agent.invoke import QAAnswer, invoke_llama3, astream_invoke_llama3
from service.agent.chain import retrieval_client
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/astream/qa", response_model=QAAnswer)
async def invoke_streaming(bodyModel: QaReqBody, req: Request):
    body = bodyModel.model_dump()
    session = body['session']
    question = body['question']

    print('start chain')
    astream = astream_invoke_llama3(session, question)

    async def event_generator():
        # {'input': 'xx'}
        # {'chat_history': []}
        # {'context: [Document()]}
        # {'answer': 'xxx'}
        async for chunk in astream:
            answer = chunk.get('answer')
            if 'answer' in chunk:
                yield "data: {\"message\": \"" + answer + "\"}" + "\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class LoadRepoReqBody(BaseModel):
    repo: str


@app.post("/stream/load_doc")
async def load_doc(bodyModel: LoadRepoReqBody):
    body = bodyModel.model_dump()
    repo = body['repo']
    retrieval_client.load_doc([repo])
