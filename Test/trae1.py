from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from langchain.chat_models import init_chat_model

model = init_chat_model("deepseek-chat", model_provider="DeepSeek")

result = model.invoke("你好")

print(result)