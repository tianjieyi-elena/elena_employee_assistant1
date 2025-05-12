import gradio as gr
from work.faq_add import *
from work.faq_query import *


def add_faq():
    with gr.Tab("csv文件上传"):
        file_input = gr.File(label="上传CSV文件", file_types=[".csv"])
        dataframe_output = gr.DataFrame(label="读取到的数据", wrap=True, headers=["问题类别", "问题", "答案"],
                                        column_widths=[10, 40, 40])
        process_button = gr.Button("读取文件")
        save_button = gr.Button("保存到知识库")
        result_text = gr.Textbox(label="处理结果")

        save_button.click(save_csv_knowledge, inputs=[dataframe_output, file_input], outputs=result_text)
        process_button.click(load_csv, inputs=[file_input], outputs=dataframe_output)