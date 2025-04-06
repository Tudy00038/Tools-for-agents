import os
from langchain_community.tools.riza.command import ExecPython
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType

# Ensure the Riza API key is set in the environment
# Alternatively, uncomment and set it here:
os.environ["RIZA_API_KEY"] = (
    "riza_01JPTGGEF235ZCTMVH4JYAJ40E_01JPTGH7JAZDXWXQB7K30H2EZW"
)

# Initialize the local LLM with Ollama

from llm_config import get_llm

llm = get_llm("code_generator")


# Define the Riza tool for executing Python code
tools = [ExecPython()]
prompt = PromptTemplate.from_template(
    """
 You are an expert Python developer who writes clean, efficient code.

    Given a user request, first break down what the user is asking.

    - If the request is unclear or vague, assume reasonable defaults (e.g., return top 10 primes).
    - If the request is impossible without clarification, respond with a clarifying question.

    Always return working Python code with comments explaining the logic.

    Example:
    Input: "Write code to do bubble sort"
    Output:
    ```python
    def bubble_sort(arr):
        '''Sorts a list using the bubble sort algorithm.'''
        ...


        """
)
# Create the agent with ZERO_SHOT_REACT_DESCRIPTION type
# This allows the agent to reason step-by-step and use tools when needed
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Enable detailed logging for debugging
)


# Function to run the agent with a user input
def run_agent(user_input):
    result = agent.invoke(user_input)
    return result


# Example usage
if __name__ == "__main__":
    # Test case 1: Generate code only
    # input1 = "Create a Python function that calculates the Fibonacci sequence."
    # print("Input:", input1)
    # print("Output:", run_agent(input1))
    # print("\n")

    # Test case 2: Generate and execute code
    input2 = "Calculate the factorial of 10."
    print("Input:", input2)
    print("Output:", run_agent(input2))
