from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.core.config import settings


def get_llm():

    llm_endpoint = HuggingFaceEndpoint(
        repo_id=settings.hf_model,
        huggingfacehub_api_token=settings.hf_token,
        task="text-generation",
        max_new_tokens=512,
        temperature=0
    )

    return ChatHuggingFace(
        llm=llm_endpoint
    )