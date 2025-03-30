import re


def select_agent(output):
    match = re.search(r"Agent Name:\s*(.+)", output)
    if match:
        return match.group(1).strip()
    return "Ambiguous"
