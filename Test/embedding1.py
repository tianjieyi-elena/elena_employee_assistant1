from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_community.embeddings import DashScopeEmbeddings

_ = load_dotenv(find_dotenv())

model_name = "text-embedding-v3"
embeddings_model = DashScopeEmbeddings(model=model_name)

embeddings = embeddings_model.embed_documents(["hello world", "hello world too!"])

len(embeddings[0])
print("count:" + str(len(embeddings)))
print("维度:" + str(len(embeddings[0])))
print("向量1" + str(embeddings[0]))
print("向量2" + str(embeddings[1]))