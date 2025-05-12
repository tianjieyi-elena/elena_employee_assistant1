from langchain.chat_models import init_chat_model

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv("C:\\Users\\86156\\Codingfuture\\employee_assistant\\.env")

from langsmith import Client

from common.llm_call import get_answer

model_test = init_chat_model(model="qwen2.5-72b-instruct", model_provider="openai")

model_judge = init_chat_model(model="qwen2.5-72b-instruct", model_provider="openai")


def target(input:dict) -> dict:
    messages = [
        {"role": "system", "content": "Answer the following question accurately"},
        {"role": "user", "content": input['问题']},
    ]
    response = get_answer(model_test,messages)
    return {"答案":response}


def judge(inputs:dict,outputs:dict,reference_outputs:dict):
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
        {"role": "user", "content": user_content}
    ]
    response = get_answer(model_judge,messages)
    return response == "CORRECT"

client = Client()

expirement_result = client.evaluate(
    target,
    data="ds-extraneous-countess-94",
    evaluators=[judge],
    experiment_prefix="before-fine-tuning",
    max_concurrency=2
)

print("done")