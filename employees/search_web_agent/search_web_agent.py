from langchain_community.tools import DuckDuckGoSearchResults
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import PromptTemplate
from .argos_translate_tool import ArgosTranslateTool

from llm_config import get_llm

llm = get_llm("search_web")


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
    If the user input contains the word 'translate', always use `argos_translate` and stop after getting the result.
    If the user input is a translation request:
    - Use only `argos_translate`
    - Once a translation is returned, stop and respond with:
    Final Answer: <translated text>

    Do not search the web or ask further questions after a successful translation.
    Use this format strictly:
    
    Question: {input}
    Thought: <your thought>
    Action: <chosen tool>
    Action Input: <input format for the chosen tool>
    Observation: <tool result>
    ... (repeat Thought/Action as needed)
    Once you have fully answered the user's question using one tool, finish with:
    Final Answer: <the final answer>
    Use a single tool whenever possible. Avoid redundant lookups. Once a complete answer is generated, finish.
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
    max_iterations=5,
)


def execute_web_search(question):
    result = agent.invoke(question)
    return result
