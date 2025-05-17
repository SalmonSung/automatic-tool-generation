from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from langgraph.constants import Send

from core.utils import *
from core.state import *
from core.configuration import Configuration
from core.create_tool_agent.graph import create_tool_agent_builder


def load_file(state: SectionState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    columns_info = get_column_info(state["orig_file_path"], index4file=configurable.index4file)
    return {"columns_info": columns_info}


def router(state: SectionState, config: RunnableConfig) -> Command[Literal["create_tool_agent_builder"]]:
    configurable = Configuration.from_runnable_config(config)
    breadth = configurable.Breadth
    breadth = 1 if breadth == 0 else breadth
    columns_infos = []
    for _ in range(breadth):
        columns_infos.append(state["columns_info"])
    return Command(goto=[
        Send("create_tool_agent_builder", {"columns_info": c})
        for c in columns_infos
    ])

def space_holder(state: SectionState, config: RunnableConfig):
    return state

builder = StateGraph(SectionState, input=SectionInput, output=SectionOutput, config_schema=Configuration)
builder.add_node("load_file", load_file)
builder.add_node("router", router)
builder.add_node("create_tool_agent_builder", create_tool_agent_builder.compile())
builder.add_node("space_holder", space_holder)

builder.add_edge(START, "load_file")
builder.add_edge("load_file", "router")
builder.add_edge("create_tool_agent_builder", "space_holder")
builder.add_edge("space_holder", END)

graph = builder.compile()
