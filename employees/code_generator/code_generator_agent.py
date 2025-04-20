import os
import json
import re
from langchain_community.tools.riza.command import ExecPython
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType, Tool
from llm_config import OllamaLLM

os.environ["RIZA_API_KEY"] = (
    "riza_01JPTGGEF235ZCTMVH4JYAJ40E_01JPTGH7JAZDXWXQB7K30H2EZW"
)


# Safe Python execution with explicit output capture
def safe_exec_python(code: str) -> str:
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        result = local_vars.get(
            "result", "Execution completed without explicit result."
        )
        return f"Execution result:\n{result}"
    except Exception as e:
        return f"Error during execution:\n{str(e)}"


# Tool definition
tools = [
    Tool.from_function(
        func=safe_exec_python,
        name="safe_exec_python",
        description="Safely execute Python code and explicitly return the output.",
    )
]

# Improved prompt template enforcing strict JSON output with required agent variables
prompt = PromptTemplate(
    template="""
You are an expert Python developer agent. You have access to the following tools:
{tool_names}

When you want to execute code, use the safe_exec_python tool via action JSON.

User Input: {input}

{agent_scratchpad}

You MUST output exactly one JSON object and NOTHING else, following one of these schemas based solely on the user's phrasing:

1) Code-Only Mode (user input begins with "Generate code "):
{"final_answer":"<escaped Python code>"}

2) Generate-and-Run Mode (user input begins with "Generate and run code "):
{"action":"safe_exec_python","action_input":"<escaped Python code>"}

Strict requirements:
- Output must be valid JSON with double-quoted keys and values only.
- Do NOT include markdown fences, backticks, commentary, or extra whitespace.
- Escape newlines in code as "\n".
- If you cannot produce valid JSON under these rules, output exactly:
{"error":"unable_to_format"}

Examples:
Input: Generate code to add 1 and 2
Output: {"final_answer":"def add(a, b):\n    return a + b\n\nresult = add(1, 2)"}

Input: Generate and run code to add 1 and 2
Output: {"action":"safe_exec_python","action_input":"def add(a, b):\n    return a + b\n\nresult = add(1, 2)"}
""",
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
)


# Agent runner function parsing JSON
def run_agent(user_input: str, model_name: str) -> str:
    llm = OllamaLLM(model=model_name)
    # Pass prompt via agent_kwargs to ensure it's used
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={"prompt": prompt},
    )

    try:
        raw = agent.invoke(user_input)
        output = (
            raw.get("output") if isinstance(raw, dict) and "output" in raw else str(raw)
        )
        text = output.strip()

        # Remove JSON fences if present
        json_text = re.sub(r"^```json\\s*|\\s*```$", "", text, flags=re.DOTALL).strip()

        data = json.loads(json_text)

        # Branch on keys
        if data.get("action") == "safe_exec_python":
            code = data["action_input"]
            exec_res = safe_exec_python(code)
            return (
                f"Generated Code:\n```python\n{code}\n```\n\n"
                f"Execution Result:\n{exec_res}"
            )

        elif "final_answer" in data:
            code = data["final_answer"]
            return f"Generated Code:\n```python\n{code}\n```"

        else:
            return output

    except json.JSONDecodeError as jde:
        return f"Failed to parse JSON output: {str(jde)}\nRaw output was:\n{text}"
    except Exception as e:
        return f"Error invoking agent: {str(e)}. Please refine your query."


# Optional local test
if __name__ == "__main__":
    tests = [
        ("Generate code to multiply two numbers", "gemma3:latest"),
        ("Generate and run code to multiply 3 and 4", "gemma3:latest"),
    ]
    for inp, model in tests:
        print("Input:", inp)
        print("Output:", run_agent(inp, model))
        print("---")
