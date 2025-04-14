from fastapi import FastAPI, Request
from pydantic import BaseModel
import sys
from pathlib import Path

# Add the root directory to sys.path BEFORE other imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))

from fastapi.middleware.cors import CORSMiddleware
from llm_config import get_llm, AGENT_MODEL_MAP
from orchestrator.orchestrator_agent import orchestrate
from orchestrator.tools.agent_selector import select_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # <-- your frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str
    selected_llms: dict


@app.post("/api/query")
async def query_agent(request: PromptRequest):
    response = orchestrate(request.prompt, request.selected_llms)
    return response
