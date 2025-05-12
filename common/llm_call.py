from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import dashscope
from http import HTTPStatus
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 我的共通
from common.llm import MyLLM

from common.my_config import MyConfig

config = MyConfig()
llm = MyLLM()

# 取得Dao信息
from dao.llm_dao import LLMDao, LLM

llm_dao = LLMDao(config.rdb_path)

# 重新排序模型
# https://help.aliyun.com/zh/model-studio/developer-reference/text-rerank-api?spm=a2c4g.11186623.0.0.7be21d1cwvGQaO


def get_selected_llm():
    selected_llm = llm_dao.get_llm_by_id(llm_dao.get_selected_llm_id())
    model = llm.get_openai_llm(selected_llm.model_name, selected_llm.api_key, selected_llm.base_url)
    return model


def test_llm(model, question):
    prompt_str = question
    prompt = ChatPromptTemplate.from_template(prompt_str)
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    result = chain.invoke({})
    return result


def get_answer(model, question):
    prompt_str = question
    prompt = ChatPromptTemplate.from_messages(prompt_str)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    result = chain.invoke({})
    return result


def generate_answer(question,reference):
    model = get_selected_llm()
    prompt_str = f"""
    上下文:
    {reference}
    问题:
    {question}
    任务：
    -请根据上下文生成对问题的回答。
    -回答简洁明了
    """
    prompt = ChatPromptTemplate.from_template(prompt_str)
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    result = chain.invoke({})
    return result