from typing import List, TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
import operator


class CodeApprovalItem(BaseModel):
    code: str = Field(description="The code to achieve the idea")
    approval: Literal["accepted", "rejected"] = Field(description="Whether the code is approved to be aligned with the idea.")


class APDFormat(BaseModel):
    ideas: List[str] = Field(description="The ideas for the further Python development.")


# =============================================================
class CTAInput(BaseModel):
    columns_info: str = Field(description="The columns info of the file you will analysis.")

class CTAOutput(BaseModel):
    code_approval_items: list

class CTAState(TypedDict):
    columns_info: str
    ideas: List[str]

    code_approval_items: Annotated[list, operator.add]
