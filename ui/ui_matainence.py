import gradio as gr
from work.knowledge_maintenance import *
from work.faq_query import *


def matainence():
    with gr.Tab("FAQ维护"):
        with gr.Row():
            export_qa_data_button = gr.Button("导出FAQ数据")
            delete_qa_data_button = gr.Button("删除所有FAQ数据")
        with gr.Row():
            maintain_result_text = gr.Textbox(label="处理结果")
        export_qa_data_button.click(export_qa, inputs=[], outputs=maintain_result_text)
        # delete_qa_data_button.click(delete_qa, inputs=[], outputs=maintain_result_text)
    with gr.Tab("文档维护"):
        with gr.Row():
            export_doc_data_button = gr.Button("导出文档数据")
            delete_doc_data_button = gr.Button("删除文档数据")

        with gr.Row():
            maintenance_result_text = gr.Textbox(label="处理结果")

        export_doc_data_button.click(
            export_doc,
            inputs=[],
            outputs=maintenance_result_text,
        )

        # delete_doc_data_button.click(
        #     delete_doc_data,
        #     inputs=[],
        #     outputs=[maintenance_result_text],
        # )