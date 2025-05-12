import configparser
import configparser
import yaml
import os

# 加载环境变量
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


class MyConfig:
    def __init__(self):
        self.rdb_path = 'rdb/km'
        self.vdb_path = "./vdb"

        self.export_dir = "./export/"
        self.backup_dir = "./backup/"
        self.config_file = "config.yaml"
        self.temp_save_dir = "./doc/"

        self.query_type_list = ["ALL", "工作时间", "考勤管理", "请假制度", "加班管理", "薪资福利", "绩效考核",
                                "员工培训与发展", "保密与竞业限制", "员工行为规范"]

        self.faq_embedding_threshold =None
        self.faq_embedding_top_k = None
        self.doc_embedding_threshold = None
        self.doc_embedding_top_k = None
        self.rerank_threshold = None
        self.rerank_top_k = None
        # self.faq_embedding_threshold = self.get_faq_embedding_threshold()
        # self.faq_embedding_top_k = self.get_faq_embedding_top_k()
        # self.doc_embedding_threshold = self.get_doc_embedding_threshold()
        # self.doc_embedding_top_k = self.get_doc_embedding_top_k()
        # self.rerank_threshold = self.get_rerank_threshold()
        # self.rerank_top_k = self.get_rerank_top_k()

        self.qa_collection_name = "qa_knowledge"
        self.doc_collection_name = "doc_knowledge"

        # qwen embedding模型  换模型在这里
        self.embedding_api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.embedding_api_key = os.environ["DASHSCOPE_API_KEY"]
        self.embedding_model_name = "text-embedding-v3"

        # BAAI  BAAI/bge-large-zh-v1.5 "BAAI/bge-m3"
        # self.embedding_api_base = "https://api.siliconflow.cn/v1/embeddings"
        # self.embedding_api_key = "sk-mueakevbkdbdzumlgpcnwnxcikyywuynuipjygpsgyadsjeu"
        # self.embedding_model_name = "BAAI/bge-large-zh-v1.5"
        self.load_config()

    def get_faq_embedding_threshold(self):
        self.load_config()
        return self.faq_embedding_threshold

    def get_faq_embedding_top_k(self):
        self.load_config()
        return self.faq_embedding_top_k

    def get_doc_embedding_threshold(self):
        self.load_config()
        return self.doc_embedding_threshold

    def get_doc_embedding_top_k(self):
        self.load_config()
        return self.doc_embedding_top_k

    def get_rerank_threshold(self):
        self.load_config()
        return self.rerank_threshold

    def get_rerank_top_k(self):
        self.load_config()
        return self.rerank_top_k

    def to_dict(self):
        return {
            'faq_embedding_threshold': self.faq_embedding_threshold,
            'faq_embedding_top_k': self.faq_embedding_top_k,
            'doc_embedding_threshold': self.doc_embedding_threshold,
            'doc_embedding_top_k': self.doc_embedding_top_k,
            'rerank_threshold': self.rerank_threshold,
            'rerank_top_k': self.rerank_top_k
        }

    def save_config(self):
        with open(self.config_file, 'w') as file:
            yaml.dump(self.to_dict(), file)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                config_data = yaml.safe_load(file)
                if config_data:
                    self.faq_embedding_threshold = float(
                        config_data.get('faq_embedding_threshold', self.faq_embedding_threshold))
                    self.faq_embedding_top_k = int(config_data.get('faq_embedding_top_k', self.faq_embedding_top_k))
                    self.doc_embedding_threshold = float(
                        config_data.get('doc_embedding_threshold', self.doc_embedding_threshold))
                    self.doc_embedding_top_k = int(config_data.get('doc_embedding_top_k', self.doc_embedding_top_k))
                    self.rerank_threshold = float(config_data.get('rerank_threshold', self.rerank_threshold))
                    self.rerank_top_k = int(config_data.get('rerank_top_k', self.rerank_top_k))
