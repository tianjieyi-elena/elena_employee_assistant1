from work.faq_query import *
from work.doc_query import *

def get_faq_answer(question):
    result = semantic_search(question)
    if result == None or len(result["metadatas"]) == 0:
        return "没答案"
    else:
        metadatas = result["metadatas"]
        answer = metadatas[0]["answer"]
        return answer


def get_doc_answer(question):
    result = doc_semantic_search(question)
    if result is None or len(result["metadatas"]) == 0:
        return "没答案"
    document = result["document"]
    reference = ""
    for doc in document:
        reference += doc + "\n"
    gen_result = generate_answer(question,reference)
    return gen_result
