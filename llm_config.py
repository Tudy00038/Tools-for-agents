# llm_config.py
from langchain_ollama import OllamaLLM

# Change this one line to use a different model
MODEL_NAME = "gemma3:latest"
# MODEL_NAME = "llama3.2:latest"
# MODEL_NAME = "mistral:latest"


def get_llm():
    return OllamaLLM(model=MODEL_NAME)
