from typing import Type, Tuple, Optional, Union
from pydantic import BaseModel
from langchain_core.runnables import Runnable
from .graph import build_graph

class StructuredEvaluator(Runnable):
    def __init__(self, llm, schema: Type[BaseModel]):
        self.schema = schema
        self.llm = llm
        self.graph = build_graph(self.llm, self.schema)

    def invoke(
        self,
        prompt: str,
        config=None,
        return_state: bool = False
    ) -> Union[BaseModel, None, Tuple[Optional[BaseModel], dict]]:

        initial_state = {
            "prompt": prompt,
            "raw_output": None,
            "parsed": None,
            "error": None,
            "retries": 0
        }

        final_state = self.graph.invoke(initial_state)

        if return_state:
            return final_state.get("parsed"), final_state

        return final_state.get("parsed")
