import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import re
from employees.github_readme_agent.github_readme_agent import execute_employee_task
from employees.search_web_agent.search_web_agent import execute_web_search
from employees.code_generator.code_generator_agent import run_agent


def route_task(agent_name, user_request):
    if agent_name == "GitHub README Summarizer":
        repo_url = extract_github_url(user_request)
        if not repo_url:
            return (
                "Clarification needed: Please provide a valid GitHub URL to summarize."
            )
        return execute_employee_task(repo_url)

    elif agent_name == "Search Web Agent":
        return execute_web_search(user_request)

    elif agent_name == "Code Generator Agent":
        if (
            "code" not in user_request.lower()
            and "function" not in user_request.lower()
        ):
            return "Clarification needed: Are you requesting code generation? Please confirm explicitly."
        return run_agent(user_request)

    else:
        return f"No implementation available yet for agent '{agent_name}'."


def extract_github_url(text):
    match = re.search(r"https://github\.com/\S+", text)
    return match.group(0) if match else None


def extract_code_from_input(text):
    match = re.search(r'Code:?"(.+?)"', text, re.DOTALL)
    return str(match.group(1)) if match else ""
