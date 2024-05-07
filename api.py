from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scripts import functions
from langchain import hub # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
import utils
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from scripts import functions
from openai import OpenAI


client = OpenAI()
llm = ChatOpenAI(model=utils.MODEL_NAME,
                temperature = 0.0,
                streaming = True)
pipeline_cache = {}
app = FastAPI()


async def loadPipeline(url):
    if url in pipeline_cache:
        return pipeline_cache[url]
    try:
        functions.getEnvVar('OPENAI_API_KEY')
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f'OPENAI API KEY not found / invalid: {str(e)}')
    try:
        docs = await functions.parseHtmlFiles(url)
        print('PARSING HTML......')
        text = await functions.splitDocuments(docs)
        print('CREATING VECTOR STORE......')
        vectorstore = functions.embedDocuments(text)
        retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        prompt = hub.pull("rlm/rag-prompt")
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        print('RAG CHAIN INITIALIZED......')
        pipeline_cache[url] = rag_chain
        return rag_chain
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Loading QA pipeline failed: {str(e)}')


async def createContent(format, topic):
    system_prompt = utils.content_creator_prompt
    question = f'format: {format}, topic: {topic}'
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}])
    return response.choices[0].message.content


class WebQA(BaseModel):
    url: str
    question: str

class ContentCreation(BaseModel):
    format: str
    topic: str


@app.post("/web_qa/")
async def web_qa(query: WebQA):
    try:
        rag_chain = await loadPipeline(query.url)
        response = rag_chain.invoke(query.question)
        return {"answer": response}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/content_creation/")
async def content_creation(query: ContentCreation):
    try:
        response = await createContent(query.format, query.topic)
        return {"text": response}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@app.post("/api/")
async def main_endpoint(query: dict):
    if 'format' in query and 'topic' in query:
        # Route to Content Creation endpoint
        return await content_creation(ContentCreation(**query))
    elif 'url' in query and 'question' in query:
        # Route to Web QA endpoint
        return await web_qa(WebQA(**query))
    else:
        raise HTTPException(status_code=400, detail="Invalid input data")
