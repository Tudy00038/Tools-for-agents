from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field

from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

llm = OllamaLLM(model="llama3.2:latest")


def generate_documentation(code: str) -> str:
    """Uses LLM to generate documentation for a given code snippet."""
    prompt = PromptTemplate(
        input_variables=["code"],
        template="Write high-quality documentation for the following code:\n\n{code}",
    )

    response = llm.invoke(prompt.format(code=code))
    return response


# Define input schema for structured agent requests
class DocumentationInput(BaseModel):
    code: str = Field(description="The code snippet to generate documentation for.")


def document_code(code: str):
    """Generates documentation for a given code snippet."""
    return generate_documentation(code)


# Define the tool for documentation generation
documentation_tool = Tool(
    name="Code Documentation Generator",
    func=document_code,
    description="Generates structured documentation for a given code snippet.",
)

llm = OllamaLLM(model="llama3.2:latest")

agent = initialize_agent(
    tools=[documentation_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True,
)


# Function to run the agent
def execute_documentation_task(code: str):
    return agent.invoke(code)


if __name__ == "__main__":
    example_code = "def add(a, b): return a + b "
    print(execute_documentation_task(example_code))
