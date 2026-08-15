from langchain.chat_models import init_chat_model

from shared.config import GROQ_API_KEY, MODEL_NAME

llm = init_chat_model(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
)

def invoke(messages):
    return llm.invoke(messages)