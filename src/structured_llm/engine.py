from typing import Type
from pydantic import BaseModel
from .graph import build_graph
from langchain_core.runnables import Runnable

class StructuredEvaluator(Runnable):
    def __init__(self, llm, schema: Type[BaseModel]):
        self.schema = schema
        self.llm = llm
        self.graph = build_graph(self.llm, self.schema)

    def invoke(self, input, config=None) -> BaseModel | None:
        initial_state = {
            "prompt": input,
            "raw_output": None,
            "parsed": None,
            "error": None,
            "retries": 0
        }

        result = self.graph.invoke(initial_state)

        return result["parsed"]