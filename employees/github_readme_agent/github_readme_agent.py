from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import OllamaLLM

from langchain_text_splitters import CharacterTextSplitter
import requests
from langchain_nomic import NomicEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


def fetch_readme_content(repo_url):
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


def chunk_readme_content(readme_content):
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return splitter.split_text(readme_content)


def summarize_readme(repo_url):
    readme_content = fetch_readme_content(repo_url)
    chunks = chunk_readme_content(readme_content)
    documents = [Document(page_content=chunk) for chunk in chunks]
    llm = OllamaLLM(model="llama3.2:latest")
    summary_chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    summary = summary_chain.invoke(documents)
    return summary["output_text"]


# Usage
repo_url = "https://github.com/catamaican/angular-scroll"
summary = summarize_readme(repo_url)
print(summary)


# Define the tool
github_summary_tool = Tool(
    name="GitHub README Summarizer",
    func=summarize_readme,
    description="Summarizes the README.md file from a provided GitHub repository URL.",
)

# Initialize LLM agent (employee)
llm = OllamaLLM(model="llama3.2:latest")

agent = initialize_agent(
    tools=[github_summary_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,  # Enables retrying if output parsing fails
)


# Modified agent_response function to accept repo_url
def agent_response(observation, repo_url):
    """
    Process the observation and return a correctly formatted response.

    Args:
        observation (str): The input or feedback the agent receives.
        repo_url (str): The GitHub repository URL to summarize.

    Returns:
        str: A response formatted with 'Thought:', 'Action:', and 'Action Input:'.
    """
    # Case 1: Handle invalid format feedback
    if "Invalid Format" in observation:
        thought = "My previous response was incorrectly formatted. I’ll ensure it includes 'Thought:', 'Action:', and 'Action Input:'."
        action = "Retry with the correct format."
        action_input = "N/A"

    # Case 2: Detect task completion (e.g., summary received)
    elif "summary" in observation.lower():  # Fixed syntax error
        thought = "I’ve received the summary from the tool. The task is complete."
        action = "Provide the final summary to the user."
        action_input = observation  # Pass the summary as the final output

    # Case 3: Default case (initiate tool usage with the provided repo_url)
    else:
        thought = "I need to summarize the GitHub repository using the tool."
        action = "Use GitHub README Summarizer"
        action_input = repo_url  # Use the provided repo_url instead of hardcoded URL

    # Format the response with required labels
    response = f"Thought: {thought}\nAction: {action}\nAction Input: {action_input}"
    return response


# Modified execute_employee_task to pass repo_url to agent_response
def save_summary_to_file(repo_url, summary_text):
    # Extract repo name
    path_parts = urlparse(repo_url).path.strip("/").split("/")
    repo_name = path_parts[-1] if len(path_parts) >= 2 else "unknown_repo"

    # Ensure summaries directory exists
    os.makedirs("summaries", exist_ok=True)

    # Save to file
    filename = f"summaries/{repo_name}_summary.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(summary_text)

    return filename


def execute_employee_task(repo_url):
    prompt = f"Summarize the GitHub repository: {repo_url}"
    raw_response = agent.run(prompt)
    formatted_response = agent_response(raw_response, repo_url)

    if "Provide the final summary" in formatted_response:
        summary = formatted_response.split("Action Input:")[1].strip()
        filepath = save_summary_to_file(repo_url, summary)
        return f"Summary saved to '{filepath}'\n\n{summary}"
    else:
        return raw_response


if __name__ == "__main__":
    example_repo = "https://github.com/Tudy00038/marketplace_dApp"
    summary = execute_employee_task(example_repo)
    print(summary)
