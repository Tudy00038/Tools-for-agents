# Import required modules from LangChain and related packages
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate

# Step 1: Initialize the local LLM with Ollama
llm = OllamaLLM(model="llama3.2:latest")

# Step 2: Initialize the DuckDuckGo Search tool
search_tool = DuckDuckGoSearchResults(name="web_search")
prompt = PromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tool:

web_search: Search the web using DuckDuckGo.

Use the following format strictly:

Question: {input}
Thought: <your thought>
Action: web_search
Action Input: <your query>
Observation: <tool result>
... (you may repeat Thought/Action cycles up to 3 times)
Final Answer: <your final answer here with references if possible>

Begin!

Question: {input}
Thought:{agent_scratchpad}
    
    """
)
# Step 3: Create the agent with the search tool and LLM
agent = initialize_agent(
    tools=[search_tool],  # List of tools the agent can use
    llm=llm,  # Local LLM instance
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent type for reasoning
    verbose=True,  # Enable detailed logs for debugging
    prompt=prompt,
    handle_parsing_errors=True,
    max_iterations=3,
)


# Step 4: Run the agent with a sample query
def execute_web_search(question):
    prompt = question
    result = agent.invoke(prompt)
    return result


# Step 5: Output the result
print(execute_web_search("What is the capital of Spain?"))
