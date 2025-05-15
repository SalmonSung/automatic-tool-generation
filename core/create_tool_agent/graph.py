import asyncio

from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from core.configuration import Configuration
from core.create_tool_agent.state import *
from core.create_tool_agent.prompts import *

def analysis_possible_direction(state: CTAState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    writer_model = configurable.writer_model
    system_prompt = prompt_analysis_possible_direction
    if writer_model == "claude-3-7-sonnet-latest":
        writer_llm = init_chat_model(model=writer_model,
                                     max_tokens=20_000,
                                     thinking={"type": "disabled", "budget_tokens": 16_000}
                                    )
    else:
        writer_llm = init_chat_model(model=writer_model)
    structured_llm = writer_llm.with_structured_output(APDFormat)
    output = structured_llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=state["columns_info"])])
    return {"ideas": output.ideas}

async def generate_code4idea(state: CTAState, config: RunnableConfig):
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

    structured_llm = writer_llm.with_structured_output(GCFormat)

    async def generate_one(idea):
        output = await structured_llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=idea)
        ])
        return output.gc_item

    tasks = [generate_one(idea) for idea in state["ideas"]]
    gc_items = await asyncio.gather(*tasks)

    return {"gc_items": gc_items}



# def idea_code_cross_check(state: CTAState, config: RunnableConfig):
#     configurable = Configuration.from_runnable_config(config)
#     planner_model = configurable.planner_model
#     system_prompt = prompt_analysis_possible_direction
#     if planner_model == "claude-3-7-sonnet-latest":
#         planner_llm = init_chat_model(model=planner_model,
#                                      max_tokens=20_000,
#                                      thinking={"type": "disabled", "budget_tokens": 16_000}
#                                     )
#     else:
#         planner_llm = init_chat_model(model=planner_model)
#     structured_llm = planner_llm.with_structured_output(APDFormat)