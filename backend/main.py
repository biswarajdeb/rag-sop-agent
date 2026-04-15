from fastapi import FastAPI
from pydantic import BaseModel
from answer import answer_question
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question:str
    history:list=[]

@app.post("/ask")
def ask(req:ChatRequest):
    answer,context=answer_question(req.question,req.history)

    new_history=req.history+[
        {"role":"user","content":req.question},
        {"role":"assistant","content":answer}
    ]

    return {"answer":answer,"context":[c.page_content for c in context],"history":new_history}
