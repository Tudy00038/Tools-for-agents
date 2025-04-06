import string
import sys
import os

# Set PYTHONPATH correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from tools.agent_selector import select_agent
from agent_router import route_task
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:latest")

# Load vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="rag_data/embeddings", embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
 You are an orchestrator agent responsible for delegating tasks to specialized agents.

    Context: {context}
    User Request: {question}

    Available agents:
    1. GitHub README Summarizer - handles GitHub repository summaries (requires URL).
    2. Search Web Agent - handles general information queries and translations.
    3. Code Generator Agent - handles code generation tasks.

    Examples:
    - "Summarize github.com/example/repo" → Agent Name: GitHub README Summarizer
    - "Explain photosynthesis" → Agent Name: Search Web Agent
    - "Translate 'Hello' from English to Spanish" → Agent Name: Search Web Agent
    - "Create Python function for Fibonacci" → Agent Name: Code Generator Agent

    Carefully analyze the user request and strictly answer with:
    Agent Name: <Agent_Name>

    If unclear, strictly answer:
    Agent Name: Ambiguous
    """,
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt_template},
    input_key="question",
)


def orchestrate(user_input):
    orchestrator_output = qa_chain.invoke({"question": user_input})["result"]
    agent_name = select_agent(orchestrator_output)

    if agent_name == "Ambiguous":
        return "Clarification needed. Please provide more details."
    elif agent_name:
        employee_response = route_task(agent_name, user_input)
        return f"Delegated to {agent_name}:\n\n{employee_response}"
    else:
        return "Could not determine the appropriate agent."


if __name__ == "__main__":
    user_request = (
        "Summarize the README for https://github.com/Tudy00038/marketplace_dApp"
        # "Who is Messi?"
        # "What is the capital of France?"
        # "Create a Python function that calculates the Fibonacci sequence. Make the function recursive."
        # "Summarize the repo."
        # "Python code to search the web."
        # "Translate 'Hello World' from English to Spanish."
    )
    response = orchestrate(user_request)
    print(response)
