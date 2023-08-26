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
    context = "Assume the following passage is an article about a topic. Rate its polarization on a scale of -5 to 5 where 5 is liberal and -5 is conservative. Also, assume a critical perspective is polar. Respond with only an integer: "
    context += message
    return chat.predict(context)

@app.get("/parse")
def document_parser(url):
    loader = AsyncHtmlLoader([url])
    docs = loader.load()
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    content = docs_transformed[0].page_content[:5000]
    arr = content.split(" ")
    
    passage = ""
    for word in arr:
        if word == "*":
            passage += ""
        if "\n" in word:
            print(word)
            print("*" * 100)

            slash = False
            newWord = ""
            for i in range(len(word)):
                if word[i] == "\\":
                    slash = True
                elif word[i] == "n" and slash:
                    slash = False
                else:
                    slash = False
                    newWord += word[i]

            passage += newWord
        else:
            word = word.replace("\\n", "")
            passage += word + " "
    print(passage)
    return passage

# Creates a summary of an article in a differing polarization
@app.get("/summarize")
def summarize(level, passage):
    # context = "Assume there exists a polarization scale from -5 to 5 such that -5 is conservative, and 5 is liberal. Assume criticism is polarizing. "
    # context += "Based on this scale, summarize the following article to be " + level + " level on this scale: "
    # context += passage
    level = int(level)
    adj = ""
    if abs(level) == 1:
        adj = "slightly"
    elif abs(level) == 2:
        adj = "slightly moderately"
    elif abs(level) == 3:
        adj = "moderately"
    elif abs(level) == 4:
        adj = "moderately heavily"
    elif abs(level) == 5:
        adj = "heavily"

    side = ""
    if level > 0:
        side = "liberal"    #consider changing to either pro-topic or against-topic
    elif level < 0:
        side = "conservative"

    context = "Summarize the following passage in a " + adj + " polarizing manner, leaning " + side + ": "
    print(context)
    context += passage





    # context = "Summarize the following passage in a heavily polarized manner from the prespective of someone who believes the Earth is flat: "
    # context += passage
    return chat.predict(context)

# def rate_sources():
#     for url in sources:
#         passage = document_parser(url)
#         rate = rate_depolarization(passage)
#         source_ratings[passage] = rate

@app.get("/depolarize")
def depolarize(passage):
    # Returns a summarization of an article that should be rated 0
    context = "Summarize the following passage without using any critical or polarizing language (Ignore any words/phrases that have nothing to do with information): "
    context += passage

    return chat.predict(context)