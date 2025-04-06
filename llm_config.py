# llm_config.py
import os
from langchain_ollama import OllamaLLM

# Define which LLM each agent should use
AGENT_MODEL_MAP = {
    "orchestrator": "gemma3:latest",
    "code_generator": "qwen2.5-coder:3b",  # updated model name from qwen2.5
    "search_web": "llama3.2:latest",
    "github_readme": "gemma3:latest",
    # add more agents if needed
}


def get_llm(agent_name: str):
    model_name = AGENT_MODEL_MAP.get(agent_name, "gemma3:latest")  # default fallback
    print(f"[LLM INIT] Agent '{agent_name}' using model: {model_name}")
    return OllamaLLM(model=model_name)
