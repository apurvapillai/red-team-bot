
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class IdeaRequest(BaseModel):
    idea: str
    round: int = 1
    history: list = []

SYSTEM_PROMPT = """You are a brutal but fair red team analyst. 
When given an idea, plan, or argument, your job is to:
1. Find the weakest points and attack them specifically
2. Give concrete failure scenarios, not vague criticism
3. Rate the idea's survivability from 0-100
4. End with ONE specific question the person must answer to defend their idea

Be sharp, specific, and ruthless. No encouragement. Format your response as:
WEAKNESSES: (bullet points)
FAILURE SCENARIO: (a specific story of how this fails)
SURVIVABILITY SCORE: X/100
DEFEND THIS: (one hard question)"""

@app.post("/redteam")
def redteam(req: IdeaRequest):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in req.history:
        messages.append(h)
    messages.append({"role": "user", "content": f"Red team this: {req.idea}"})

    response = requests.post("http://localhost:11434/api/chat", json={
        "model": "mistral",
        "messages": messages,
        "stream": False
    })

    result = response.json()
    reply = result["message"]["content"]
    return {"response": reply, "round": req.round}

