import sys
import os
import re

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Agent functions
from employees.github_readme_agent.github_readme_agent import (
    execute_employee_task_single_input,
)
from employees.search_web_agent.search_web_agent import execute_web_search
from employees.code_generator.code_generator_agent import run_agent


def route_task(agent_name, user_request, model_name):
    """
    Routes the request to the appropriate agent based on agent_name.
    Handles agent-specific formatting and output extraction.
    """

    if agent_name == "GitHub README Summarizer":
        # GitHub agent uses a single input string that combines repo_url and model_name
        tool_input_str = f"repo_url='{user_request}' model_name='{model_name}'"
        return execute_employee_task_single_input(tool_input_str)

    elif agent_name == "Search Web Agent":
        response = execute_web_search(user_request, model_name)
        # If response is a dict, extract 'output'
        if isinstance(response, dict) and "output" in response:
            return response["output"]
        return str(response)

    elif agent_name == "Code Generator Agent":
        if (
            "code" not in user_request.lower()
            and "function" not in user_request.lower()
        ):
            return (
                "Clarification needed: Are you requesting code generation? "
                "Please confirm explicitly."
            )

        raw_response = run_agent(user_request, model_name)

        # If response is a dict (e.g. {'input': ..., 'output': ...}), extract 'output'
        if isinstance(raw_response, dict) and "output" in raw_response:
            return raw_response["output"]
        return str(raw_response)

    else:
        return f"No implementation available yet for agent '{agent_name}'."


def extract_github_url(text):
    match = re.search(r"https://github\.com/\S+", text)
    return match.group(0) if match else None


def extract_code_from_input(text):
    match = re.search(r'Code:?"(.+?)"', text, re.DOTALL)
    return str(match.group(1)) if match else ""
