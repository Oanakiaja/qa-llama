from pydantic import BaseModel
from fastapi import FastAPI

from service.agent.invoke import QAAnswer, invoke_llama3

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "llama3"}


class QaReqBody(BaseModel):
    session: str
    question: str = None


@app.post("/qa", response_model=QAAnswer)
async def invoke(bodyModel: QaReqBody):
    body = bodyModel.model_dump()
    session = body['session']
    question = body['question']
    return invoke_llama3(session, question)
