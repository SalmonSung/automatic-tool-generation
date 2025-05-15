from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from core.utils import *
from core.state import *
from core.configuration import Configuration

def load_file(state: SectionState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    columns_info = get_column_info(state["orig_file_path"], index4file=configurable.index4file)
    return {"columns_info": columns_info}

def router(state: SectionState, config: RunnableConfig):
    pass

builder = StateGraph(SectionState, input=SectionInput, output=SectionOutput, config_schema=Configuration)

