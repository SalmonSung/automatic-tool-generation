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
> 👉 Check how to get started with [LangGraph Studio](example.link) for this project
