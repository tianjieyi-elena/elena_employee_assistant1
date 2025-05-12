# 系统包
import numpy as np
import pandas as pd
import gradio as gr

# 我的共通
from common.my_chroma import My_Chroma
from common.llm_call import *
from common.my_config import MyConfig

config = MyConfig()
chroma_db = My_Chroma()

# DAO
from dao.doc_dao import KnowledgeFileDAO

knowledge_file_dao = KnowledgeFileDAO()

# work
# from work.faq_add import save_one_faq


def doc_load_filename_dropdown():
    objects = knowledge_file_dao.get_all_knowledge_files()
    if len(objects) == 0:
        return ["ALL"]
    print(objects)

    catalog_list = [obj[1] for obj in objects]
    catalog_list.append("ALL")
    return catalog_list


def doc_normal_search_knowledge():
    pass


def doc_load_all_knowledge():
    pass


def doc_df_search_result_select():
    pass


def doc_semantic_search(query="",filename="All",keyword="",top_k=None,threshold=None):
    if not top_k:
        top_k = config.get_doc_embedding_top_k()
    if not threshold:
        threshold = config.get_doc_embedding_threshold()
    collection = chroma_db.doc_collection
    if query == "":
        query_str = None
    else:
        query_str = [query]

    if filename == "ALL":
        where_str = None
    else:
        where_str = {
            "filename": {
                "$eq": filename
            }
        }

    if keyword == "":
        where_document_str = None
    else:
        where_document_str = {
            "$contains": keyword
        }

    results = collection.query(
        query_texts=query_str,
        n_results=top_k,
        where=where_str,
        where_document=where_document_str
    )

    if results:
        filtered_results = {
            key: [val[0][i] for i in range(len(results["distances"][0]))
                  if (results["distances"][0][i] < threshold) and (val is not None) and key != "included"]
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


def doc_semantic_search_for_ui(query="",filename="All",keyword="",top_k=None,threshold=None):
    if not top_k:
        top_k = config.get_doc_embedding_top_k()
    if not threshold:
        threshold = config.get_doc_embedding_threshold()
    results = doc_semantic_search(query, filename,  keyword, top_k=top_k, threshold=threshold)
    if results is None:
        return None, "没有检索到相关知识！"
    else:
        ids = results["ids"]
        metadatas = results["metadatas"]
        documents = results["documents"]
        distances = results["distances"]

    df = pd.DataFrame({
        'ID': ids,
        '文件名': [meta["filename"] for meta in metadatas],
        '分段内容': documents,
        '向量距离': distances
    })
    ui_df = gr.Dataframe(
        label="搜索结果",
        value=df,
        wrap=True,
        column_widths=[10, 5, 30, 5]
    )
    return ui_df, "检索成功！"


def doc_delete_one_search_result():
    pass


def doc_rerank_knowledge():
    pass


def generate_question():
    pass


def doc_update_one_knowledge():
    pass


def doc_delete_one_knowledge():
    pass


def doc_generate_answer():
    pass


def doc_add_to_faq():
    pass


