# Guide: How to Use as a Package

1. **Copy into your project**  
   Clone or copy the `automatic-tool-generation` module into your project directory.

2. **Initialize and run the agent**  
   Use the following code to run the agent from within your Python script:
   ```python
   import uuid
   from langgraph.checkpoint.memory import MemorySaver
   from core.graph import builder
   import asyncio
   from dotenv import load_dotenv

   load_dotenv()

   file_path = "<your_file_path_here>"

   agent = AgentBuilder()
   results = asyncio.run(agent.run(file_path))
   ```

3. **(Optional) Set custom configuration**  
   You can customize how the agent behaves by passing arguments to `AgentBuilder`:
   ```python
   class AgentBuilder:
       def __init__(self,
                    planner_provider="openai",
                    planner_model="o3-mini",
                    writer_provider="openai",
                    writer_model="gpt-4.1-nano",
                    file_type="CSV",
                    index4file="true",
                    breadth=2):
           ...
   ```
   Adjust parameters like `planner_model`, `writer_model`, or `breadth` to fit your use case.
