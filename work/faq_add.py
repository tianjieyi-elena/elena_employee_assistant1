import pandas as pd
import os
from uuid import uuid4
from datetime import datetime

from common.my_config import MyConfig
config = MyConfig()

from common.my_chroma import My_Chroma
my_chroma = My_Chroma()


def load_csv(file, start_row=1):
    try:
        if file is None:
            return "请上传一个有效的csv文件！"
        df = pd.read_csv(file.name, skiprows=start_row - 1)
        df.columns = ["问题类别", "问题", "答案"]
        return df
    except Exception as e:
        return f"读取文件时出错: {e}"


def save_csv_knowledge(df, file):
    collections = my_chroma.qa_collection

    now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")

    file_all_name = file.name
    file_name = os.path.basename(file_all_name)
    print("文件名：" + file_name)

    for index, row in df.iterrows():
        page_content = f"""问题类别：{row['问题类别']}\n问题：{row['问题']}"""
        metadata = {
            "query_type": row['问题类别'],
            "question": row['问题'],
            "answer": row['答案'],
            "create_date": date_str,
            "file_name": file_name,
            "comment": ""
        }
        uuid = str(uuid4())
        print("当前存储：" + row['问题'])
        collections.add(
            documents=[page_content],
            metadatas=[metadata],
            ids=[uuid]
        )
    return "保存成功！"

