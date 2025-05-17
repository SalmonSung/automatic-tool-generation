from typing import List, TypedDict, Literal, Annotated, Optional
from pydantic import BaseModel, Field
import operator

class SectionInput(BaseModel):
    orig_file_path: str = Field(description="Path to the file you want to analyze")

class SectionOutput(BaseModel):
    orig_file_path: str = Field(description="Path to the file you want to analyze")

class SectionState(TypedDict):
    orig_file_path: str
    columns_info: str
    code_approval_items: Annotated[list, operator.add]