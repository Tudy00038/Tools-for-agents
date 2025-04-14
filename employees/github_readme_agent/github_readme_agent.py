############################
# github_readme_agent.py
############################

import os
import re
import requests
from urllib.parse import urlparse

# LangChain / Ollama / Tools imports
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

# The following two classes are from your environment; adapt imports if needed
from langchain_text_splitters import CharacterTextSplitter
from langchain_nomic import NomicEmbeddings
from langchain_community.vectorstores import FAISS

############################
# 1) HELPER FUNCTIONS
############################


def fetch_readme_content(repo_url: str) -> str:
    """Fetches README.md content from either main or master branch."""
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]
    branches = ["main", "master"]
    for branch in branches:
        raw_url = (
            repo_url.replace("github.com", "raw.githubusercontent.com")
            + f"/{branch}/README.md"
        )
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text
    raise FileNotFoundError(
        f"README.md not found in branches 'main' or 'master' at {repo_url}"
    )


def chunk_readme_content(readme_content: str) -> list[str]:
    """Splits the README content into manageable chunks for summarization."""
    # Using CharacterTextSplitter or RecursiveCharacterTextSplitter
    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return splitter.split_text(readme_content)


############################
# 2) CORE SUMMARIZE FUNCTION
############################


def summarize_readme(repo_url: str, model_name: str) -> str:
    """
    Summarizes the README of the given repo using the dynamic model specified by model_name.
    """
    # 1) Create the LLM
    llm = OllamaLLM(model=model_name)

    # 2) Fetch & chunk the README
    readme_content = fetch_readme_content(repo_url)
    chunks = chunk_readme_content(readme_content)
    documents = [Document(page_content=chunk) for chunk in chunks]

    # 3) Summarize with a map_reduce chain
    summary_chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    summary = summary_chain.invoke(documents)

    return summary["output_text"]


############################
# 3) TOOL WRAPPER FUNCTION
############################


def summarize_readme_single_input(input_str: str) -> str:
    """
    A single-argument wrapper for the ReAct agent.
    Expects input_str to look like:
      repo_url='https://github.com/catamaican/gamification' model_name='gemma3:latest'

    We'll parse out the repo_url and model_name, then call summarize_readme(repo_url, model_name).
    """
    # Use regex to find each argument
    url_match = re.search(r"repo_url=['\"]([^'\"]+)['\"]", input_str)
    model_match = re.search(r"model_name=['\"]([^'\"]+)['\"]", input_str)

    if not url_match:
        return "ERROR: No repo_url found in input_str."
    if not model_match:
        return "ERROR: No model_name found in input_str."

    repo_url = url_match.group(1)
    model_name = model_match.group(1)

    # Now call the original 2-argument function
    return summarize_readme(repo_url, model_name)


############################
# 4) DEFINE THE TOOL (ReAct style)
############################
github_summary_tool = Tool(
    name="GitHub README Summarizer",
    func=summarize_readme_single_input,
    description="Summarizes the README.md file. Provide input like: repo_url='...' model_name='...'",
)


############################
# 5) SAVE SUMMARY TO FILE
############################
def save_summary_to_file(repo_url: str, summary_text: str) -> str:
    """Saves the summary text to a .txt file named after the repository."""
    path_parts = urlparse(repo_url).path.strip("/").split("/")
    repo_name = path_parts[-1] if len(path_parts) >= 2 else "unknown_repo"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    summaries_dir = os.path.join(script_dir, "summaries")
    os.makedirs(summaries_dir, exist_ok=True)

    filename = os.path.join(summaries_dir, f"{repo_name}_summary.txt")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(summary_text)
        return filename
    except Exception as e:
        print(f"Error writing file: {e}")
        return "Error saving file."


############################
# 6) OPTIONAL: ReAct local agent usage
############################
def execute_employee_task_single_input(input_str: str) -> str:
    """
    Example function to show how you might run a local ReAct agent with the single-argument approach.
    `input_str` must contain both `repo_url` and `model_name`.
    """
    # 1) Create an LLM
    local_llm = OllamaLLM(model="gemma3:latest")

    # 2) Build an agent that can call the summarizer tool
    local_agent = initialize_agent(
        tools=[github_summary_tool],
        llm=local_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )

    # 3) Agent run with the single string
    raw_response = local_agent.run(input_str)

    # 4) Optionally store the summary to a file if the agent's final answer is indeed the summary
    # This depends on how your ReAct agent is structured.
    # If `raw_response` is the summary, you might parse out the repo_url from input_str again:
    url_match = re.search(r"repo_url=['\"]([^'\"]+)['\"]", input_str)
    if url_match:
        repo_url = url_match.group(1)
        save_summary_to_file(repo_url, raw_response)

    return raw_response


############################
# 7) Local Test
############################
if __name__ == "__main__":
    test_input = "repo_url='https://github.com/catamaican/gamification' model_name='gemma3:latest'"
    result = execute_employee_task_single_input(test_input)
    print("Final agent response:\n", result)
