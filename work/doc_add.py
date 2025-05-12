import pandas as pd
import gradio as gr
import os
from uuid import uuid4
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# 共通设定
from common.my_config import MyConfig
config = MyConfig()

from common.my_chroma import My_Chroma
chroma_db = My_Chroma()

# Dao
from dao.doc_dao import KnowledgeFileDAO
knowledge_file_dao = KnowledgeFileDAO()

def save_to_vector_db(df,file):
    collection = chroma_db.doc_collection
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    file_all_name = file.name
    file_name = os.path.basename(file_all_name)
    for index, row in df.iterrows():
        page_content = row["分段结果"]

        metadata = {
            "filename": file_name,
            "create_date": dt_string,
            "comment":""
        }
        uuid = str(uuid4())
        print("hang :" + str(index))
        collection.add(documents=[page_content],metadatas=[metadata],ids=[uuid])
    knowledge_file_dao.insert_knowledge_file(file_name)
    return "文件添加成功"


def read_pdf(file):
    loader = PyPDFLoader(file)
    document = loader.load()

    text = "\n\n".join([doc.page_content for doc in document])
    return text


def split_text(text,chunk_size=300,chunk_overlap=30):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.create_documents([text])
    df = pd.DataFrame([text.page_content for text in texts],columns=['分段结果'])
    return df