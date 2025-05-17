from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.constants import Send
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage

from core.create_tool_agent.idea2code.state import *
from core.create_tool_agent.idea2code.prompts import *
from core.configuration import Configuration


async def generate_code4idea(state: I2CState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    writer_model = configurable.writer_model
    system_prompt = prompt_generate_code4idea.format(columns_info=state["columns_info"])

    if writer_model == "claude-3-7-sonnet-latest":
        writer_llm = init_chat_model(
            model=writer_model,
            max_tokens=20_000,
            thinking={"type": "disabled", "budget_tokens": 16_000}
        )
    else:
        writer_llm = init_chat_model(model=writer_model)
    structured_llm = writer_llm.with_structured_output(GC4IFormat)
    output = await structured_llm.ainvoke([SystemMessage(system_prompt), HumanMessage(content=state["idea"])])
    return {"idea": state["idea"], "code": output.code}



async def idea_code_cross_check(state: I2CState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    planner_model = configurable.planner_model
    system_prompt = prompt_idea_code_cross_check.format(idea=state["idea"])
    if planner_model == "claude-3-7-sonnet-latest":
        planner_llm = init_chat_model(model=planner_model,
                                     max_tokens=20_000,
                                     thinking={"type": "enabled", "budget_tokens": 16_000}
                                    )
    else:
        planner_llm = init_chat_model(model=planner_model)
    structured_llm = planner_llm.with_structured_output(ICCCFormat)
    output = await structured_llm.ainvoke([SystemMessage(system_prompt), HumanMessage(content=state["code"])])
    return {"code_approval_items": [CodeApprovalItem(code=output.code, approval=output.approval)]}
    # return Command(update=,
    #                goto=END)

idea2code_builder = StateGraph(I2CState, input=I2CInput, output=I2COutput)
idea2code_builder.add_node("generate_code4idea", generate_code4idea)
idea2code_builder.add_node("idea_code_cross_check", idea_code_cross_check)

idea2code_builder.add_edge(START, "generate_code4idea")
idea2code_builder.add_edge("generate_code4idea", "idea_code_cross_check")
idea2code_builder.add_edge("idea_code_cross_check", END)

# async def generate_code4idea(state: CTAState, config: RunnableConfig):
#     configurable = Configuration.from_runnable_config(config)
#     writer_model = configurable.writer_model
#     system_prompt = prompt_generate_code4idea.format(columns_info=state["columns_info"])
#
#     if writer_model == "claude-3-7-sonnet-latest":
#         writer_llm = init_chat_model(
#             model=writer_model,
#             max_tokens=20_000,
#             thinking={"type": "disabled", "budget_tokens": 16_000}
#         )
#     else:
#         writer_llm = init_chat_model(model=writer_model)
#
#     structured_llm = writer_llm.with_structured_output(GCFormat)
#
#     async def generate_one(idea):
#         output = await structured_llm.ainvoke([
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=idea)
#         ])
#         return output.gc_item
#
#     tasks = [generate_one(idea) for idea in state["ideas"]]
#     gc_items = await asyncio.gather(*tasks)
#
#     return {"gc_items": gc_items}