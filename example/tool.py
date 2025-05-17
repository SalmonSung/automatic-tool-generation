import math

from typing import Annotated
from langchain_core.tools import tool, Tool


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b

@tool
def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@tool
def sin(a: float) -> float:
    """Take the sine of a number."""
    return math.sin(a)

@tool
def cos(a: float) -> float:
    """Take the cosine of a number."""
    return math.cos(a)

@tool
def radians(a: float) -> float:
    """Convert degrees to radians."""
    return math.radians(a)

@tool
def exponentiation(a: float, b: float) -> float:
    """Raise one number to the power of another."""
    return a**b

@tool
def sqrt(a: float) -> float:
    """Take the square root of a number."""
    return math.sqrt(a)

@tool
def ceil(a: float) -> float:
    """Round a number up to the nearest integer."""
    return math.ceil(a)

# @tool
# def python_repl_tool(
#     code: Annotated[str, "The python code to execute to generate your chart."],
# ):
#     """Use this to execute python code. If you want to see the output of a value,
#     you should print it out with `print(...)`. This is visible to the user."""
#     try:
#         result = repl.run(code)
#     except BaseException as e:
#         return f"Failed to execute. Error: {repr(e)}"
#     result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
#     return (
#         result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
#     )

tools = [
    add,
    multiply,
    divide,
    subtract,
    sin,
    cos,
    radians,
    exponentiation,
    sqrt,
    ceil,
    # search_tool,
    # repl_tool
]
#
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_experimental.utilities import PythonREPL
#
#
#
# search = DuckDuckGoSearchRun()
# python_repl = PythonREPL()
#
# repl_tool = Tool(
#     name="python_repl",
#     description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
#     func=python_repl.run,
# )
#
# search_tool = Tool(
#     name="search_engine",
#     description="A search engine you can search for.",
#     func=search.invoke,
# )