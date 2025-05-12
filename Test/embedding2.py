import requests
import json

url = "https://api.siliconflow.cn/v1/embeddings"

payload = {
    "model": "BAAI/bge-large-zh-v1.5",
    "input": "hello word!",
    "encoding_format": "float"
}
headers = {
    "Authorization": "Bearer sk-mmogsjstkaxqecszuqusrrwlxmqdekqylcaqasperfixbfsw",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

json_data = json.loads(response.text)
print(json_data['data'][0]['embedding'])