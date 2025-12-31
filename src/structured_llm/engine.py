from typing import Type
from pydantic import BaseModel
from llm import GetChatModel
from .graph import build_graph

class StructuredEvaluator:
    def __init__(self, model_path, schema: Type[BaseModel]):
        self.schema = schema,
        self.llm = GetChatModel(model_path).get_model()
        self.graph = build_graph(self.llm, self.schema)

    def run(self, prompt: str) -> BaseModel | None:
        initial_state = {
            "prompt": prompt,
            "raw_output": None,
            "parsed": None,
            "error": None,
            "retries": 0
        }

        result = self.graph.invoke(initial_state)

        return result['parsed']