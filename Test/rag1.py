from langchain_community.document_loaders import PyPDFLoader

file_path = (
    "公司管理规定.pdf"
)

loader = PyPDFLoader(file_path)
documents = loader.load()

# 连接文本
text = "\n\n".join([doc.page_content for doc in documents])

print(text)
