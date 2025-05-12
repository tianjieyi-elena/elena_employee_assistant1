from langchain_openai import ChatOpenAI

class MyLLM:

    def __init__(self):
        pass

    def get_openai_llm(self, model_name, api_key, base_url):
        llm = ChatOpenAI(
            api_key=api_key,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url=base_url,  # 填写DashScope base_url
            model=model_name
        )
        return llm