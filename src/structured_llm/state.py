from typing_extensions import TypedDict
from typing import Optional
from pydantic import BaseModel, Field

class GraphState(TypedDict):
    prompt : str
    raw_output: Optional[str]
    parsed: Optional[BaseModel]
    error: Optional[str]
    retries: int