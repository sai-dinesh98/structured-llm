from langchain_huggingface.chat_models.huggingface import ChatHuggingFace
from langchain_huggingface.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, pipeline
import torch

class GetChatModel:
    def __init__(self, model_path):
        self.model_path = model_path

    def get_model(self):

        model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            trust_remote_code=False,
            dtype=torch.float16,
            device_map="auto",
        )

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=self.model_path,
            max_new_tokens=500,
            return_full_text=False,
            do_sample=True,
            temperature=0.7,
        )

        
        llm = HuggingFacePipeline(pipeline=pipe)
        chat = ChatHuggingFace(llm=llm)

        return chat
        