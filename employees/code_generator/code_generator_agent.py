import time
from typing import Tuple
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools.riza.command import ExecPython

# Prompt templates for code and tests generation
CODE_TEMPLATE = PromptTemplate(
    input_variables=["user_request"],
    template="""
You are a Python coding assistant.
When given a request, output ONLY the Python function implementation—no explanation, comments, or any other text.
Your response MUST begin with "def " and end at the last line of the function definition.

Request: {user_request}
""",
)

TEST_TEMPLATE = PromptTemplate(
    input_variables=["function_code", "user_request"],
    template="""
You are a Python testing assistant.
Write a pytest-style test suite for the following function. Cover edge cases and typical inputs.

Function code:
{function_code}

Tests must import the function and define one or more test_ functions. Output ONLY the test code block, no prose.
""",
)

# Safe execution tool
test_exec = ExecPython()


def make_code_agent(
    model_name: str, ollama_url: str = "http://localhost:11434"
) -> Tuple[LLMChain, LLMChain]:
    """
    Returns two chains:
    1. code_chain: generates function code
    2. test_chain: generates pytest tests for the code
    """
    llm = ChatOllama(model=model_name, base_url=ollama_url)
    code_chain = LLMChain(llm=llm, prompt=CODE_TEMPLATE)
    test_chain = LLMChain(llm=llm, prompt=TEST_TEMPLATE)
    return code_chain, test_chain


def generate_and_validate(
    chain_tuple: Tuple[LLMChain, LLMChain], request: str, max_retries: int = 2
) -> str:
    """
    Generates Python code, writes tests, and executes them in a loop until passing or max_retries.
    Returns the validated function code.
    """
    code_chain, test_chain = chain_tuple
    for attempt in range(1, max_retries + 1):
        # 1. Generate code
        function_code = code_chain.run(user_request=request).strip()

        # 2. Generate tests
        test_code = test_chain.run(
            function_code=function_code, user_request=request
        ).strip()

        # 3. Combine code + tests
        full_script = f"{function_code}\n\n{test_code}"

        # 4. Execute tests
        result = test_exec.run(full_script)

        # Check for pytest failures
        if "ERROR" not in result and "FAIL" not in result:
            return function_code
        # Brief pause before retry
        time.sleep(1)
    # If all retries fail, raise with last result
    raise RuntimeError(f"Validation failed after {max_retries} attempts:\n{result}")


# Example usage
if __name__ == "__main__":
    code_chain, test_chain = make_code_agent("gemma3:latest")
    try:
        code = generate_and_validate(
            (code_chain, test_chain),
            "Write a function that calculates the Fibonacci sequence up to n terms",
        )
        print(code)
    except RuntimeError as e:
        print(str(e))
