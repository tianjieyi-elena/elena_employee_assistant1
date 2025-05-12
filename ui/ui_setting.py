import gradio as gr
from work.setting import *
from work.faq_query import *

def setting():
    with gr.Tabs():
        with gr.Tab("向量搜索设定"):
            embedding_query_setting()
        with gr.Tab("大模型设定"):
            llm_setting()


def embedding_query_setting():
    return gr.Textbox(label="向量搜索设定")


def llm_setting():
    with gr.Tabs():
        with gr.Tab("大模型列表"):
            with gr.Blocks():
                with gr.Row():
                    df_llm = gr.DataFrame(
                        label='大模型列表',
                        headers=["ID", "模型名", "API_Key", "Base_url"],
                        value=load_llm()
                    )
                with gr.Row():
                    btn_update_llm = gr.Button("刷新")
                    btn_use_llm = gr.Button("使用该模型")

                    btn_delete_llm = gr.Button("删除该模型")
                with gr.Row():
                    txt_selected_llm = gr.Textbox(
                        label="选中的大模型ID",
                        visible=True,
                        value=get_selected_llm_id()
                    )
                    txt_list_result = gr.Textbox(label="处理结果")
                btn_use_llm.click(fn=use_llm, inputs=txt_selected_llm, outputs=txt_list_result)
                df_llm.select(
                    fn=select_llm, inputs=df_llm, outputs=txt_selected_llm)
                btn_update_llm.click(fn=load_llm, inputs=None, outputs=df_llm)
                btn_delete_llm.click(fn=delete_llm, inputs=txt_selected_llm, outputs=txt_list_result)
        with gr.Tab("大模型添加"):
            with gr.Blocks():
                with gr.Row():
                    model_name = gr.Textbox(label="模型名称")
                    api_key = gr.Textbox(label="API Key")
                    base_url = gr.Textbox(label="Base URL")
                with gr.Row():
                    txt_question = gr.Textbox(label="测试问题")
                    gr.Examples(
                        examples=["你好，你是谁？", "今天是2023年10月6日，星期五，4天前是星期几，仅返回数字。"],
                        inputs=txt_question
                    )
                with gr.Row():
                    btn_test = gr.Button("测试")
                    btn_save = gr.Button("保存")
                with gr.Row():
                    txt_add_result = gr.Textbox(label="处理结果")
                btn_save.click(fn=save_model, inputs=[model_name, api_key, base_url], outputs=txt_add_result)
                btn_test.click(fn=test_model, inputs=[model_name, api_key, base_url, txt_question],
                               outputs=txt_add_result)