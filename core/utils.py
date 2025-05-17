import pandas as pd
from typing import Literal
from pydantic import BaseModel



def get_column_info(csv_path: str, index4file) -> str:
    """
    Returns:
    - A string listing the column names and index name (if applicable)
    """
    if index4file == "true":
        df = pd.read_csv(csv_path, index_col=0)
        index_name = df.index.name or "<Unnamed Index>"
        columns = list(df.columns)
        return f"Index: {index_name}\nColumns: {', '.join(columns)}"
    else:
        df = pd.read_csv(csv_path)
        columns = list(df.columns)
        return f"Columns: {', '.join(columns)}"


def pydantic2dict(item: BaseModel | list) -> dict:
    if isinstance(item, list):
        item = item[0]

    #Dict form
    item = item.model_dump()

    #Keys list
    key = list(item.keys())
    return item