import pandas as pd
import os
from datetime import datetime
import gradio as gr

from common.my_config import MyConfig
config = MyConfig()

from common.my_chroma import My_Chroma
my_chroma = My_Chroma()

df_global = pd.DataFrame({
    'ID': [],
    'document': []
})

def semantic_search(query="", keyword="", top_k=None, em_threshold=None):
    if not top_k:
        top_k = 1
    if not em_threshold:
        em_threshold = config.get_faq_embedding_threshold()
    collections = my_chroma.qa_collection
    if query == "":
        query_str = None
    else:
        query_str = [query]
    if keyword == "":
        where_document_str = None
    else:
        where_document_str = {
            "$contains": keyword
        }

    results = collections.query(
        query_texts=query_str,
        n_results=top_k,
        where_document=where_document_str
    )

    if results:
        filtered_results = {
            key: [val[0][i] for i in range(len(results["distances"][0]))
                  if (results["distances"][0][i] < em_threshold) and (val is not None)]
            for key, val in results.items()
        }
        return {
            "ids": filtered_results["ids"],
            "documents": filtered_results["documents"],
            "metadatas": filtered_results["metadatas"],
            "distances": filtered_results["distances"]
        }
    else:
        return None


def one_semantic_search(query="", keyword="", embedding_top_k=None, threshold=None):
    if not embedding_top_k:
        embedding_top_k = 1
    if not threshold:
        threshold = config.get_faq_embedding_threshold()
    results = semantic_search(query, keyword, top_k=embedding_top_k, em_threshold=threshold)
    if results is None:
        return None, "没有检索到相关知识！"
    else:
        ids = results["ids"]
        metadatas = results["metadatas"]
        # documents = results["documents"]
        distances = results["distances"]
    # global df_global
    # df_global = df_global.drop(df_global.index)
    # df_global['ID'] = ids
    # df_global['document'] = documents

    df = pd.DataFrame({
        'ID': ids,
        '问题类别': [meta["query_type"] for meta in metadatas],
        '问题': [meta["question"] for meta in metadatas],
        'distances': distances
    })
    ui_df = gr.Dataframe(
        label="搜索结果",
        value=df,
        wrap=True,
        column_widths=[10,5,10,20]
    )
    return ui_df, "检索成功！"


def normal_search_knowledge(query_type="ALL", keyword=""):
    collections = my_chroma.qa_collection
    if query_type != "ALL":
        where_str = {
            "query_type": {
                "$eq": query_type
            }
        }
    else:
        where_str = None

    if keyword == "":
        where_document_str = None
    else:
        where_document_str = {
            "$contains": keyword
        }
    results = collections.get(where=where_str, where_document=where_document_str)

    if results:
        ids = results["ids"]
        metadatas = results["metadatas"]
        query_type = [meta["query_type"] for meta in metadatas]
        question = [meta["question"] for meta in metadatas]
        distances = results["distances"]
        df = pd.DataFrame({
            'ID': ids,
            '问题类别': query_type,
            '问题': question,
            "向量距离": distances,
        })
        ui_df = gr.DataFrame(label="搜索结果", wrap=True, value=df, column_widths=[10, 5, 20, 10])
        return ui_df


def clear_one_query():
    return "", "", ""


def load_all_knowledge():
    collections = my_chroma.qa_collection
    results = collections.get()
    if results:
        ids = results["ids"]
        metadatas = results["metadatas"]
        query_type = [meta["query_type"] for meta in metadatas]
        question = [meta["question"] for meta in metadatas]
        df = pd.DataFrame({
            'ID': ids,
            '问题类别': query_type,
            '问题': question
        })
    ui_df = gr.DataFrame(label="搜索结果", wrap=True, value=df, column_widths=[10, 5, 20])
    return ui_df


def df_search_result_select(event: gr.SelectData, df: pd.DataFrame):
    one_row_id = event.row_value[0]
    row = df[df['ID'] == one_row_id].index.tolist()[0]
    one_row_question = df.loc[row, "问题"]
    query_type = df.loc[row, "问题类别"]
    collections = my_chroma.qa_collection
    results = collections.query(
        query_texts=[one_row_question],
        where={
            "query_type": query_type
        },
        n_results=1
    )
    if results:
        metadatas = results["metadatas"][0]
        one_row_answer = metadatas[0]["answer"]
        one_row_comment = metadatas[0]["comment"]
        one_row_filename = metadatas[0]["file_name"]
        one_row_create_date = metadatas[0]["create_date"]
        return one_row_id, one_row_question, one_row_answer, one_row_comment, one_row_filename, one_row_create_date
    else:
        return one_row_id, one_row_question, "", "", "", ""

def update_one_knowledge(row_id,row_question,row_answer,row_comment):
    collections = my_chroma.qa_collection
    collections.update(
        ids=row_id,
        metadatas=[{
            "answer": row_answer,
            "comment": row_comment,
            "question": row_question,
            "create_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }]
    )
    return "更新成功！"


def delete_one_knowledge(row_id):
    collections = my_chroma.qa_collection
    collections.delete(ids=row_id)
    return "删除成功！"


def get_all_models():
    pass