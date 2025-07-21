A modular AI agentic workflow platform built using LangChain, with a FastAPI backend and Vue.js frontend, designed to run on local LLMs via Ollama (e.g., LLaMA 3, Mistral, Qwen, Gemma). This project implements an Orchestrator Agent that interprets user input and routes tasks to specialized Employee Agents such as:

🧠 Question Answering Agent (search)

🌐 Translation Agent (via Argos Translate)

⚙️ Code Execution Agent (safe, sandboxed Python execution)

🔍 GitHub README Analyzer (fetches and summarizes repos)

The system emphasizes privacy-first AI, with all models and tools running locally — ideal for users or organizations needing secure, offline intelligent assistants. Each tool in the ecosystem is modular, making it easy to extend with new agents or upgrade existing ones.

Use cases include:

Personal AI assistants

Local LLM research setups

Secure enterprise automation

Educational experimentation with agentic workflows

The platform supports storing prompt logs, saving chat history, and visualizing agent routing logic. Whether you're exploring autonomous AI systems or building your own assistant, this project provides a robust starting point with modern tooling and open-source principles.
