# Automatic Tool Generation

**Automatic Tool Generation** is a subproject of [*Create Data Scientist Agent*](docs/hyperproject.md)

The main goal of this project is to **automatically and independently generate tools** for use by LLM agents. Rather than manually predefining tools for every possible use case, this project introduces a pipeline that can:

1. **Analyze** the task type  
2. **Ideate** potential solutions  
3. **Generate** appropriate Python tools  
4. **Validate** them against sample data

This approach enables more flexible, scalable, and intelligent agents that can adapt to diverse data analysis scenarios without requiring human experts in tool preparation.

> [!WARNING]
> **CLI tools are still under active development**, and functionality is currently limited.
> For full experience, consider using **LangGraph Studio** instead.
>
> 👉 Check how to get started with [LangGraph Studio](doc/how_to/use_langgraph_dev.md) for this project

# Quick Start

1. **Set up your environment**  
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your own API keys and configuration as needed.

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Use LangGraph Studio**  
   If you want to use LangGraph Studio for a better development experience:  
   ```bash
   pip install 'langgraph-cli[inmem]'
   ```
   >This step does not require creating account.
   >It run a local server and open a web browser to control the agent

# Table of Content 
- Usage Guideline:
   - [LangGraph Dev(recommand)](docs/how_to/use_langgraph_dev.md)
   - [Cli tool](docs/how_to/use_cli.md)
   - [Use in Your Project](docs/how_to/use_as_package.md)
