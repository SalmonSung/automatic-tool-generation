## AgentBuilder Configuration

The `AgentBuilder` class provides a configurable interface for setting up your agent's behavior. Below is the default configuration, optimized for OpenAI users (due to its popularity):

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
        # Configurable parameters
        self.planner_provider = planner_provider
        self.planner_model = planner_model
        self.writer_provider = writer_provider
        self.writer_model = writer_model
        self.file_type = file_type
        self.index4file = index4file
        self.breadth = breadth
```

### Parameter Explanations

- **`file_type`**:  
  The type of the original input file. Currently, only `CSV` files are supported.

- **`index4file`**:  
  Indicates whether the file includes an index column (typically the first column).  
  Accepts `"true"` or `"false"` as string values.

- **`breadth`**:  
  Defines how many agents to invoke in parallel.  
  Each agent will generate three ideas. Ideally resulting in three tools if the code passes LLM-based evaluation.
