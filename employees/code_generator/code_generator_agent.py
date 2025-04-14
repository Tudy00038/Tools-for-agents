import os
from langchain_community.tools.riza.command import ExecPython
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType

# Already imported here once:
from llm_config import OllamaLLM

os.environ["RIZA_API_KEY"] = (
    "riza_01JPTGGEF235ZCTMVH4JYAJ40E_01JPTGH7JAZDXWXQB7K30H2EZW"
)

tools = [ExecPython()]

prompt = PromptTemplate.from_template(
    """
    You are an expert Python developer who writes clean, efficient code.

    Given a user request, first break down what the user is asking.

    - If the request is unclear, assume reasonable defaults (e.g., return top 10 primes).
    - If the request is impossible without clarification, respond with a clarifying question.

    Always return working Python code with comments explaining the logic.

    Example:
    Input: "Write code to do bubble sort"
    Output:
    ```python
    def bubble_sort(arr):
        ...
    ```
    """
)


def run_agent(user_input, model_name):
    # 1) Create the Ollama LLM with the user-selected model
    llm = OllamaLLM(model=model_name)

    # 2) Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # 3) Invoke the agent
    result = agent.invoke(user_input)
    return result


# Optional local test
if __name__ == "__main__":
    input_text = "Calculate the factorial of 10."
    print("Input:", input_text)
    print("Output:", run_agent(input_text, "gemma3:latest"))
