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
from .tools.agent_selector import select_agent
from .agent_router import route_task
from llm_config import get_llm
from llm_config import OllamaLLM

llm = get_llm("orchestrator")


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
    chain_type_kwargs={"prompt": prompt_template, "document_variable_name": "context"},
    input_key="question",
)


def orchestrate(user_input, selected_llms):
    # Dynamically select LLM for orchestrator
    orchestrator_llm_model = selected_llms.get("orchestrator", "gemma3:latest")
    orchestrator_llm = OllamaLLM(model=orchestrator_llm_model)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
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
        llm=orchestrator_llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt_template},
        input_key="question",
    )

    orchestrator_output = qa_chain.invoke({"question": user_input})["result"]
    agent_name = select_agent(orchestrator_output)

    if agent_name == "Ambiguous":
        return "Clarification needed."
    elif agent_name:
        # Select the LLM for the chosen agent dynamically
        agent_llm_model = selected_llms.get(agent_name, "gemma3:latest")
        employee_response = route_task(agent_name, user_input, agent_llm_model)
        return f"Delegated to {agent_name} (using {agent_llm_model}):\n\n{employee_response}"
    else:
        return "Could not determine agent."


if __name__ == "__main__":
    user_request = (
        # "Summarize the README for https://github.com/catamaican/gamification"
        # "Who is Messi?"
        # "What is the capital of France?"
        # "Create a Python function that calculates the factorial of a number. Make the function recursive."
        # "Summarize the repo."
        # "Python code to search the web."
        "Translate 'I am 19 years old' from English to Spanish."
    )
    response = orchestrate(user_request)
    print(response)
