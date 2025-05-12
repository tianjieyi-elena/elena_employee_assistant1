import gradio as gr
from work import faq_query
from work import chat

def add_message(history,message):
    for x in message["files"]:
        history.append({"role": "user", "content": {"path": x}})
    if message["text"] is not None:
        history.append({"role":"user","content":message["text"]})
    return history,gr.MultimodalTextbox(value=None,interactive=True)


def bot(history, knowledge_type):
    my_question = history[-1]["content"]
    if knowledge_type == "FAQ":
        # 调用FAQ查询
        result = chat.get_faq_answer(my_question)
    else:
        # 调用chat查询
        result = chat.get_doc_answer(my_question)
    msg_no_data = {"role":"assistant","content":""}
    msg_no_data["content"]=result
    history.append(msg_no_data)
    return history


with gr.Blocks(title="企业问答助手") as demo:
    gr.Markdown("# 企业问答助手")
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        type="messages",
        show_copy_button=True,
        scale=1
    )
    chat_input = gr.MultimodalTextbox(
        interactive=True,
        file_count="multiple",
        placeholder="Enter message or upload files",
        show_label=False,
    )
    examples = gr.Examples(
        examples=[
            "公司的工作时间是如何安排的","早退30分钟怎么处理"
        ],
        inputs=[chat_input]
    )
    chat_msg = chat_input.submit(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input],
    )
    radio_type = gr.Radio(
        choices=["FAQ", "文件"],
        value="FAQ",
        label="回复类型"
    )
    bot_msg = chat_msg.then(
        bot,
        [chatbot, radio_type],
        chatbot,
        api_name="bot_response"
    )
    bot_msg.then(
        lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])


if __name__ == "__main__":
    demo.launch()