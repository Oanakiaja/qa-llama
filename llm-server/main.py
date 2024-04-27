from typing import Union

from fastapi import FastAPI

from chain import invoke_llama3

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "llama3"}


@app.get("/invoke/{message}")
async def invoke(message: Union[str, None] = None):
    return invoke_llama3(message)