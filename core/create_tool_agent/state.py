from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field


class GCItem(BaseModel):
    idea: str = Field(description="The idea for the further Python development.")
    code: str = Field(description="The code to achieve the code")


class CTAInput(BaseModel):
    columns_info: str = Field(description="The columns info of the file you will analysis.")


class CTAState(TypedDict):
    columns_info: str
    ideas: List[str]
    gc_items: List[GCItem]


class APDFormat(BaseModel):
    ideas: List[str] = Field(description="The ideas for the further Python development.")


class GCFormat(BaseModel):
    gc_item: GCItem
