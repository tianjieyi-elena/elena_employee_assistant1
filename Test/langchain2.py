from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

model = init_chat_model("deepseek-chat", model_provider="DeepSeek")

prompt_str = """
你是一个笑话大师，请给我讲一个笑话。
主题是：{topic}
"""

prompt = ChatPromptTemplate.from_template(prompt_str)
output_parser = StrOutputParser()
chain = prompt | model | output_parser

for s in chain.stream({"topic": "程序员"}):
    print(s, end="|", flush=True)