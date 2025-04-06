from langchain_community.tools import DuckDuckGoSearchResults
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from .argos_translate_tool import ArgosTranslateTool

llm = OllamaLLM(model="llama3.2:latest")

# Existing DuckDuckGo tool
search_tool = DuckDuckGoSearchResults(name="web_search")

# New translation tool
translate_tool = ArgosTranslateTool()

# Update the agent to have multiple tools
tools = [search_tool, translate_tool]

# Updated prompt to indicate both tools clearly
prompt = PromptTemplate.from_template(
    """
   You are an assistant with access to two tools:
    
    web_search: Search the web using DuckDuckGo.
    argos_translate: Translate text from one language to another (format: 'text|from_language_code|to_language_code', using ISO codes like 'en', 'es', 'fr', 'de', etc.).

    Given the user input, choose the correct tool to resolve the task.

    Use this format strictly:
    
    Question: {input}
    Thought: <your thought>
    Action: <chosen tool>
    Action Input: <input format for the chosen tool>
    Observation: <tool result>
    ... (repeat Thought/Action as needed)
    Final Answer: <final answer with results>
    
    Begin!
    
    Question: {input}
    Thought:{agent_scratchpad}
    """
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    prompt=prompt,
    handle_parsing_errors=True,
    max_iterations=3,
)


def execute_web_search(question):
    result = agent.invoke(question)
    return result
