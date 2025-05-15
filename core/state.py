from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field

class SectionInput(BaseModel):
    orig_file_path: str = Field(description="Path to the file you want to analyze")

class SectionOutput(BaseModel):
    orig_file_path: str = Field(description="Path to the file you want to analyze")

class SectionState(TypedDict):
    orig_file_path: str
    columns_info: str