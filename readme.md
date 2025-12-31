Structured LLM (LangGraph-based)

Reliable structured outputs from local LLMs using schema validation, retries, and self-repair.

structured-llm is a lightweight Python package that guarantees schema-correct outputs from LLMs that do not natively support structured output (e.g. local HuggingFace models like Phi-3, Gemma, Mistral).

It uses LangGraph to:

Generate LLM output

Validate it against a Pydantic schema

Automatically retry + repair invalid JSON outputs

Return a strongly-typed Python object

✨ Why this exists

Most local LLMs:

❌ Do not support function calling

❌ Do not enforce JSON schemas

❌ Often return malformed JSON

This package gives you:

✅ Schema-validated outputs
✅ Automatic retries
✅ Self-repair prompts
✅ Model-agnostic design
✅ Works with local + hosted LLMs

🧠 How it works (high-level)
Prompt
  ↓
LLM Node
  ↓
Parse Node (Pydantic)
  ↓
┌───────────────┐
│ Valid?        │── yes ──▶ DONE
│               │
│ Invalid?      │── no ──▶ Repair Node → retry
└───────────────┘


Powered by LangGraph state machines, not brittle regex parsing.

📦 Installation
Editable install (recommended for development)
git clone https://github.com/<your-username>/structured_llm.git
cd structured_llm
pip install -e .


After this, you can import it from any directory.

🗂 Project structure
structured_llm/
├── pyproject.toml
├── README.md
└── src/
    └── structured_llm/
        ├── __init__.py
        ├── engine.py        # High-level API
        ├── graph.py         # LangGraph definition
        ├── llm.py           # LLM adapters
        ├── nodes.py         # llm / parse / repair nodes
        ├── state.py         # Graph state
        └── utils.py

🚀 Quick start
1️⃣ Define a schema
from pydantic import BaseModel, Field

class EvaluationSchema(BaseModel):
    feedback: str = Field(description="Feedback within 100 words")
    score: int = Field(ge=0, le=10)

2️⃣ Load your local LLM
from structured_llm.llm import GetGemmaModel

model = GetGemmaModel(
    model_path="path/to/Phi3-mini-instruct"
).get_model()


Any HuggingFace causal LM works.

3️⃣ Run structured evaluation
from structured_llm.engine import StructuredEvaluator

evaluator = StructuredEvaluator(
    llm=model,
    schema=EvaluationSchema,
    max_retries=2
)

result = evaluator.invoke(
    prompt="Evaluate the language quality of the following essay...",
)

4️⃣ Access typed output
print(result.parsed.feedback)
print(result.parsed.score)


✅ result.parsed is a real Pydantic object, not raw JSON.

🧪 What happens on bad JSON?

If the model outputs something like:

Sure! Here's the evaluation:
{
  feedback: "Great essay"
  score: 8


The system will automatically:

Detect schema failure

Generate a repair prompt

Retry with corrected JSON

Stop after max_retries

No manual parsing. No crashes.

🔧 Configuration
Parameter	Description
schema	Pydantic model defining output
max_retries	Max repair attempts
llm	Any LangChain-compatible chat model
❌ What this does NOT do

❌ Does not rely on OpenAI / Anthropic

❌ Does not require function calling

❌ Does not use fragile regex parsing

🧩 When should I use this?

Use structured-llm when:

You run local models

You need guaranteed JSON

You want schema safety

You don’t trust raw LLM outputs

🔮 Future roadmap

 Generic StructuredLLM base class

 CLI (structured-llm eval essay.txt)

 Streaming support

 Metrics / tracing hooks

 Multi-schema routing

📜 License

MIT License

🙌 Credits

Built with:

LangGraph

LangChain

Pydantic