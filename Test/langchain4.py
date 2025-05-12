from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

_ = load_dotenv(find_dotenv())

model = init_chat_model("deepseek-chat", model_provider="DeepSeek")

prompt_template = ChatPromptTemplate([
    ("system", "你是一个笑话大师."),
    ("user", "请给我讲一个{topic}的笑话.")
])

output_parser = StrOutputParser()
chain = prompt_template | model | output_parser

for s in chain.stream({"topic": "程序员"}):
    print(s, end="", flush=True)