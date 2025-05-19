prompt_response2file = """
You are a senior developer tasked with identifying and refactoring duplicate or similar functions by merging them into a multiple unique implementation.

Always ensure files are loaded using their full file paths.
Please provide comprehensive docstring for each method.
Please add decorate @tool 
Please add every tool into tools list like the following example.

Format your output like the following example:
```python
from langchain_core.tools import tool, Tool

@tool
def add(a: float, b: float) -> float:
    \"\"\"Add two numbers.\"\"\"
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    \"\"\"Multiply two numbers.\"\"\"
    return a * b
    
tools = [add, multiply]
```

"""