from typing import List, TypedDict, Literal, Annotated, Optional
from pydantic import BaseModel, Field
import operator


class R2FFormat(BaseModel):
    code: str = Field(description="The Python code after your process.")


# ==========================================================
class SectionInput(BaseModel):
    orig_file_path: str = Field(description="Path to the file you want to analyze")


class SectionOutput(BaseModel):
    clean_code_sheet: str = Field(description="The Python code after your process.")


class SectionState(TypedDict):
    orig_file_path: str
    columns_info: str

    code_approval_items: Annotated[list, operator.add]

    clean_code_sheet: str
