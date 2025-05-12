from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langsmith import Client
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv("C:\\Users\\86156\\Codingfuture\\employee_assistant\\.env")

# 模型构建
model_judge_use = init_chat_model("deepseek-chat", model_provider="DeepSeek")

from work.chat import get_faq_answer, get_doc_answer
from common.llm_call import get_answer

def target(inputs: dict) -> dict:
    response = get_faq_answer(inputs["问题"])
    #response = get_doc_answer(inputs["问题"])
    print("当前问题:" + inputs["问题"])
    return {"答案": response}

def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):

    eval_instructions = "You are an expert professor specialized in grading students' answers to questions."

    user_content = f"""You are grading the following question:
    {inputs['问题']}
    Here is the real answer:
    {reference_outputs['答案']}
    You are grading the following predicted answer:
    {outputs['答案']}
    Respond with CORRECT or INCORRECT:
    Grade:
    """

    messages = [
        {"role": "system", "content": eval_instructions},
        {"role": "user", "content": user_content},
    ]

    response = get_answer(model_judge_use, messages)
    return response == "CORRECT"

client = Client()

# After running the evaluation, a link will be provided to view the results in langsmith
experiment_results = client.evaluate(
    target,
    data="employee_test_5",
    evaluators=[
        correctness_evaluator,
        # can add multiple evaluators here
    ],
    experiment_prefix="employee_test_5",
    max_concurrency=2,
)
print("评测完成！")
