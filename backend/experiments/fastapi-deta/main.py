from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
# from langchain.document_loaders import AsyncChromiumLoader
# from langchain.document_transformers import BeautifulSoupTransformer
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer

app = FastAPI()
chat = ChatOpenAI(openai_api_key="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")
sources = ["https://oceanservice.noaa.gov/facts/earth-round.html", 
           "https://nautil.us/why-do-people-believe-the-earth-is-flat-305667/",
           "https://wiki.tfes.org/Flat_Earth_-_Frequently_Asked_Questions"]

source_ratings = {}

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
    context = "Assume the following passage is a scientific article about a topic. Also, assume a critical perspective is poalr. Rate its polarization on a scale of -5 to 5 where 5 is very liberal and -5 is very conservative with just an integer: "
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
    arr = content.split(" ")
    content = content.strip("*")
    print(content)
    print("*"*50)
    print(arr)
    passage = ""
    for word in arr:
        if word == "\\n":
            passage += " "
        else:
            word = word.replace("\\n", "")
            passage += word + " "
        

    # context = "Can you remove the special characters from this and remove \\n: "
    # context += content
    # prediction = chat.predict(context)
    # print("*"*100)
    # print(prediction)
    return passage

# Creates a summary of an article in a differing polarization
@app.get("/summarize")
def summarize(level, url):
    context = ""
    context += document_parser(url)
    return chat.predict(context)

def rate_sources():
    for url in sources:
        passage = document_parser(url)
        rate = rate_depolarization(passage)
        source_ratings[passage] = rate

@app.get("/depolarize")
def depolarize(passage):
    # Returns a summarization of an article that should be rated 0
    context = "Summarize the following passage without using any critical or polarizing language (Ignore any words/phrases that have nothing to do with information): "
    context += passage

    return chat.predict(context)