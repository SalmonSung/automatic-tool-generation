import os
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.constants import Send

from core.utils import *
from core.state import *
from core.prompts import *
from core.configuration import Configuration
from core.create_tool_agent.graph import create_tool_agent_builder
from config import APP_PATH_RESULT


def load_file(state: SectionState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    columns_info = get_column_info(state["orig_file_path"], index4file=configurable.index4file)
    return {"columns_info": columns_info}


def router(state: SectionState, config: RunnableConfig) -> Command[Literal["create_tool_agent_builder"]]:
    configurable = Configuration.from_runnable_config(config)
    breadth = configurable.breadth
    breadth = 1 if breadth == 0 else breadth
    columns_infos = []
    for _ in range(breadth):
        columns_infos.append(state["columns_info"])
    return Command(goto=[
        Send("create_tool_agent_builder", {"columns_info": c})
        for c in columns_infos
    ])


def format_response(state: SectionState, config: RunnableConfig):
    code_approval_items_dict = []
    for item in state["code_approval_items"]:
        code_approval_items_dict.append(pydantic2dict(item))
    # state["code_approval_items"] = code_approval_items_dict
    state["code_approval_items"].clear()
    state["code_approval_items"].extend(code_approval_items_dict)
    return state


def response2file(state: SectionState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    writer_model = configurable.writer_model
    system_prompt = prompt_response2file
    if writer_model == "claude-3-7-sonnet-latest":
        writer_llm = init_chat_model(model=writer_model,
                                     max_tokens=20_000,
                                     thinking={"type": "disabled", "budget_tokens": 16_000}
                                     )
    else:
        writer_llm = init_chat_model(model=writer_model)
    structured_llm = writer_llm.with_structured_output(R2FFormat)
    output = structured_llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content="\n".join(item["code"] for item in state["code_approval_items"]))])

    file_name = f"tool_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    file_path = os.path.join(APP_PATH_RESULT, file_name)
    with open(file_path, "w") as f:
        f.write(output.code)
    return {"clean_code_sheet": output.code, "tool_save_path": file_path}


builder = StateGraph(SectionState, input=SectionInput, output=SectionOutput, config_schema=Configuration)
builder.add_node("load_file", load_file)
builder.add_node("router", router)
builder.add_node("create_tool_agent_builder", create_tool_agent_builder.compile())
builder.add_node("format_response", format_response)
builder.add_node("response2file", response2file)

builder.add_edge(START, "load_file")
builder.add_edge("load_file", "router")
builder.add_edge("create_tool_agent_builder", "format_response")
builder.add_edge("format_response", "response2file")
builder.add_edge("response2file", END)

graph = builder.compile()
