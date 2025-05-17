import asyncio

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.constants import Send
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from core.configuration import Configuration
from core.create_tool_agent.state import *
from core.create_tool_agent.prompts import *
from core.create_tool_agent.idea2code.graph import idea2code_builder

async def analysis_possible_direction(state: CTAState, config: RunnableConfig):
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
    output = await structured_llm.ainvoke([SystemMessage(content=system_prompt), HumanMessage(content=state["columns_info"])])
    return {"ideas": output.ideas}

def idea_router(state: CTAState, config: RunnableConfig) -> Command[Literal["idea2code"]]:
    return Command(goto=[
        Send("idea2code", {"idea": i, "columns_info": state["columns_info"]})
        for i in state["ideas"]
    ])

def test_code(state: CTAState, config: RunnableConfig):
    return {"code_approval_items": [state["code_approval_items"]]}
    # return Command(update=, goto=END)


create_tool_agent_builder = StateGraph(CTAState, input=CTAInput, output=CTAOutput)
create_tool_agent_builder.add_node("analysis_possible_direction", analysis_possible_direction)
create_tool_agent_builder.add_node("idea_router", idea_router)
create_tool_agent_builder.add_node("idea2code", idea2code_builder.compile())
create_tool_agent_builder.add_node("test_code", test_code)

create_tool_agent_builder.add_edge(START, "analysis_possible_direction")
create_tool_agent_builder.add_edge("analysis_possible_direction", "idea_router")
create_tool_agent_builder.add_edge("idea2code", "test_code")
create_tool_agent_builder.add_edge("test_code", END)


