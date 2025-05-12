import pandas as pd
from datetime import datetime

from common.my_config import MyConfig
config = MyConfig()

from common.my_chroma import My_Chroma
my_chroma = My_Chroma()


def export_qa():
    collections = my_chroma.qa_collection
    results = collections.get()
    if results is not None:
        query_type = [doc["query_type"] for doc in results["metadatas"]]
        question = [doc["question"] for doc in results["metadatas"]]
        answer = [doc["answer"] for doc in results["metadatas"]]
        create_date = [doc["create_date"] for doc in results["metadatas"]]
        file_name = [doc["file_name"] for doc in results["metadatas"]]
        comment = [doc["comment"] for doc in results["metadatas"]]
        df = pd.DataFrame({"问题类别": query_type, "问题": question, "答案": answer,"文件名":file_name,"创建日期":create_date,"备注":comment})
        file_name = "knowledge_data" + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"
        df.to_excel(config.export_dir + file_name, index=False)
        return "导出成功" + file_name


def export_doc():
    collections = my_chroma.doc_collection
    results = collections.get()
    if results is not None:
        page_content = results["documents"]
        create_date = [doc["create_date"] for doc in results["metadatas"]]
        file_name = [doc["filename"] for doc in results["metadatas"]]
        comment = [doc["comment"] for doc in results["metadatas"]]
        df = pd.DataFrame({"文本内容": page_content, "文件名": file_name, "创建日期": create_date,"备注":comment})
        file_name = "doc_data" + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"
        df.to_excel(config.export_dir + file_name, index=False)
        return "导出成功" + file_name
