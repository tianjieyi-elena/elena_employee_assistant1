# 页面函数
import gradio as gr

from work.doc_add import *

# 共通设定
from common.my_config import MyConfig

config = MyConfig()

def ui_add_doc():
    with gr.Blocks():
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    pdf_file_input = gr.File(label="上传PDF文件", file_types=[".pdf"])
                with gr.Row():
                    btn_read_pdf = gr.Button("PDF文件读取")

            with gr.Column(scale=1):
                with gr.Row():
                    chunk_size_input = gr.Number(label="文本块大小", value=200)
                    overlap_input = gr.Number(label="文本块重叠", value=20)
                with gr.Row():
                    btn_split = gr.Button("文件分割")
                    btn_save_vector_db = gr.Button("存储到向量数据库")
                with gr.Row():
                    doc_work_result_text = gr.Textbox(label="处理结果", lines=1, interactive=True)
        with gr.Row():
            with gr.Column(scale=1):
                pdf_read_result_text = gr.Textbox(label="文件读取结果", lines=20, interactive=True)
            with gr.Column(scale=1):
                df_split_result = gr.DataFrame(label="分割结果", wrap=True)


        btn_save_vector_db.click(
            save_to_vector_db,
            inputs=[df_split_result, pdf_file_input],
            outputs=[doc_work_result_text],
        )

        btn_read_pdf.click(
            read_pdf,
            inputs=[pdf_file_input],
            outputs=[pdf_read_result_text],
        )
        btn_split.click(
            split_text,
            inputs=[pdf_read_result_text, chunk_size_input, overlap_input],
            outputs=[df_split_result],
        )
