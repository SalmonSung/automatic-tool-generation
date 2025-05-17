from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field

class CodeApprovalItem(BaseModel):
    code: str = Field(description="The code to achieve the idea")
    approval: Literal["true", "false"] = Field(description="Whether the code is approved to be aligned with the idea.")

class GC4IFormat(BaseModel):
    idea: str = Field(description="The idea for the further Python development.")
    code: str = Field(description="The code to achieve the code")

class ICCCFormat(BaseModel):
    code: str = Field(description="The code to achieve the idea")
    reason: str = Field(description="The reason for why the code can achieve the idea")
    approval: Literal["true", "false"] = Field(description="Whether the code is approved to be aligned with the idea.")

#====================================================================================]
class I2CInput(BaseModel):
    idea: str = Field("The idea for the further Python development.")
    columns_info: str

class I2COutput(BaseModel):
    code_approval_items: List[CodeApprovalItem]

class I2CState(TypedDict):
    idea: str
    columns_info: str

    code: str
    approval: Literal["accepted", "rejected"]
    code_approval_items: List[CodeApprovalItem]