from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import AsyncChromiumLoader
# from langchain.document_transformers import BeautifulSoupTransformer
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer

app = FastAPI()
chat = ChatOpenAI(openai_api_key="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")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/query")
def get_response(message):
    return chat.predict(message)

@app.get("/rate")
def rate_depolarization(message):
    context = "Assume the following passage is a scientific article about a topic. Rate its polarization on a scale of -5 to 5 where 5 is very liberal and -5 is very conservative with just an integer: "
    context += message
    return chat.predict(context)

@app.get("/parse")
def document_parser(url):
    # Load HTML
    # loader = AsyncChromiumLoader([url])
    # html = loader.load()
    # bs_transformer = BeautifulSoupTransformer()
    # docs_transformed = bs_transformer.transform_documents(html,tags_to_extract=["p", "li", "div", "a"])

    # return docs_transformed

    loader = AsyncHtmlLoader([url])
    docs = loader.load()
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    content = docs_transformed[0].page_content[:5000]
    print(content)

    context = "Can you remove the special characters from this and remove \\n: "
    context += content
    prediction = chat.predict(context)
    print("*"*100)
    print(prediction)
    return prediction
