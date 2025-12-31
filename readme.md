Structured LLM (LangGraph)

Robust structured output extraction for local LLMs using LangGraph, Pydantic, and automatic retry and repair.

Structured LLM is a lightweight Python package that makes non-JSON-compliant LLMs usable in production by enforcing structured outputs through schema validation and automatic repair loops. It is designed specifically for local and open-source language models that do not reliably follow strict output formats.

Why this exists

Most local and open-source LLMs do not consistently return valid JSON, even when prompted carefully. This becomes a serious problem when building pipelines that require structured data.

This module solves that problem by:

Calling the LLM

Parsing the output into a strict schema

Automatically repairing invalid JSON

Retrying in a controlled loop

Returning either a validated object or a clean failure

You never silently fail.

Key features

Automatic retry loop using LangGraph

Schema-driven parsing using Pydantic

Self-healing JSON repair prompts

Works with any local or remote LLM

Model-agnostic design

Deterministic and debuggable behavior

Designed for CPU and GPU local inference

High-level flow

LLM generates output
→ Output is parsed into schema
→ If valid, return structured object
→ If invalid, generate repair prompt
→ Retry until success or retry limit

Installation

Editable install (recommended during development):

git clone https://github.com/sai-dinesh98/structured-llm.git

cd structured-llm
pip install -e .

After this, the package can be imported from any directory.

Basic usage

Step 1: Define your output schema

Use Pydantic to define the structure you want from the LLM.

Example:

class EvaluationSchema(BaseModel):
feedback: str
score: int

Step 2: Load your local LLM

Example using a HuggingFace-based local model:

from llm import GetGemmaModel

model_path = "path/to/local/model"
llm = GetGemmaModel(model_path).get_model()

The only requirement is that the model exposes an invoke(prompt) method that returns text.

Step 3: Build the structured execution graph

from structured_llm.engine import build_structured_graph

graph = build_structured_graph(
llm=llm,
schema=EvaluationSchema,
max_retries=2
)

Step 4: Run inference

result = graph.invoke({
"prompt": "Evaluate the language quality of this essay",
"raw_output": None,
"parsed": None,
"error": None,
"retries": 0,
})

result["parsed"] will either be:

AI a valid Pydantic object

or None if all retries fail

What problems this solves

LLM outputs markdown instead of JSON

LLM adds explanations or extra text

Invalid types or missing fields

Silent parsing failures

Unbounded retry loops

When to use this

Use this package if:

You work with local or open-source LLMs

You need reliable structured output

You cannot depend on provider-native function calling

You want full control over retries and validation

When not to use this

You may not need this package if:

You only use models with native structured output support

You fully trust the model to always return valid JSON

Extensibility

The design allows you to:

Swap schemas dynamically

Add logging or telemetry nodes

Plug into larger agent systems

Add streaming or tool-based LLMs

Extend the repair strategy

Roadmap

Generic high-level StructuredRunner API

Improved JSON extraction before parsing

Streaming support

PyPI release

Example notebooks and demos

License

MIT License

Author

Sai Dinesh
Systems and Control | AI Systems | LangGraph and Local LLMs