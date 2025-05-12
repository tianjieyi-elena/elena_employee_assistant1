import sqlite3
from datetime import datetime
from common.my_config import MyConfig

config = MyConfig()


class KnowledgeFileDAO:
    def __init__(self):
        self.db_path = config.rdb_path
        # self._create_table()

    def insert_knowledge_file(self, file_name):
        # 自动获取当前日期并格式化
        create_date = datetime.now().strftime("%Y-%m-%d")
        query = "INSERT INTO knowledge_file(file_name, create_date) VALUES (?, ?);"

        with sqlite3.connect(self.db_path, uri=True) as conn:
            result = conn.execute(query, (file_name, create_date))
            # conn.close()
            return result

    def get_all_knowledge_files(self, uri=True):
        query = "SELECT * FROM knowledge_file;"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

        return rows

    def delete_knowledge_file(self, file_id):
        query = "DELETE FROM knowledge_file WHERE file_id=?;"
        with sqlite3.connect(self.db_path, uri=True) as conn:
            conn.execute(query, (file_id,))
