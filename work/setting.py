import pandas as pd
import gradio as gr

from common.my_config import MyConfig
from dao.llm_dao import LLMDao, LLM
from common.llm import MyLLM
import common.llm_call as llm_call

config = MyConfig()

llm_dao = LLMDao(config.rdb_path)


def select_llm(evt: gr.SelectData, df: pd.DataFrame):
    selected_index = evt.index[0]
    selected_row = df.iloc[selected_index]
    return selected_row['ID']


def get_selected_llm_id():
    return llm_dao.get_selected_llm_id()


def use_llm(llm_id):
    llm_dao.set_selected_llm_id(llm_id)


def load_llm():
    objects = llm_dao.get_all_llms()
    if len(objects) == 0:
        return None
    df = pd.DataFrame().from_records([obg.__dict__ for obg in objects])
    # print(df.values)

    df.rename(
        columns={df.columns[0]: 'ID', df.columns[1]: '模型名', df.columns[2]: 'API_Key', df.columns[3]: 'Base_url'},
        inplace=True)
    return df


def delete_llm(llm_id):
    llm_dao.delete_llm(llm_id)
    return "模型删除成功！"


def save_model(model_name, api_key, base_url):
    llm = LLM()
    llm.model_name = model_name
    llm.api_key = api_key
    llm.base_url = base_url
    llm_dao.insert_llm(llm)
    return "模型保存成功！"

def test_model(model_name, api_key, base_url, question):
    my_llm = MyLLM()
    model = my_llm.get_openai_llm(model_name, api_key, base_url)
    result = llm_call.test_llm(model, question)

    return result