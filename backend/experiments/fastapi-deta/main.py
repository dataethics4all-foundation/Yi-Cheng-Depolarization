from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

app = FastAPI()
chat = ChatOpenAI(openai_api_keys="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")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/query")
def get_response(message):
    result = chat.generate(SystemMessage(content="message"))
    return result
