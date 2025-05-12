import gradio as gr
from work.faq_query import *
from ui import ui_query
from ui import ui_add
from ui import ui_matainence
from ui import ui_setting
from ui import ui_add_doc


with gr.Blocks(title="企业问答助手") as demo:
    gr.Markdown("# 企业问答助手")
    with gr.Tabs():
        with gr.Tab("单条问题回答"):
            ui_query.query_faq()
        with gr.Tab("FAQ知识添加"):
            ui_add.add_faq()
        with gr.Tab("文件知识添加"):
            ui_add_doc.ui_add_doc()
        with gr.Tab("知识维护"):
            ui_matainence.matainence()
        with gr.Tab("设定"):
            ui_setting.setting()

if __name__ == "__main__":
    demo.launch()