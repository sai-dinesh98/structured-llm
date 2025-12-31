from typing import Type
from pydantic import BaseModel
from .state import GraphState
from .utils import extract_json

def llm_node(state: GraphState, llm):
    response = llm.invoke(state["prompt"])
    return {
        "raw_output": response.content
    }

def parse_node(state: GraphState, schema: Type[BaseModel]):
    try:
        raw_json = extract_json(state['raw_output'])
        parsed = schema.model_validate_json(raw_json)
        return {"parsed": parsed, "error": None}
    except Exception as e:
        return {"parsed": None, "error": str(e)}
    
def repair_node(state:GraphState, llm, schema: Type[BaseModel]):
    repair_prompt = f"""
The following output was supposed to be a valid JSON matching this schema:

{schema.model_json_schema()}

But it failed with this error:
{state['error']}

fix the output so that it is VALID JSON ONLY.

Rules:
- If JSON is incomplete or truncated, reconstruct it
- No markdown
- No backticks
- No explanations
- Must match the schema exactly

Broken output:
{state['raw_output']}
"""
    response = llm.invoke(repair_prompt)

    return {
        "raw_output": response.content,
        "retries": state["retries"] + 1,
        "error": None
    }