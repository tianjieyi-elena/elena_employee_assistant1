import gradio as gr
from work.setting import *
from work.faq_add import *
from work.knowledge_maintenance import *
from work.faq_query import *
from work.doc_add import *
from work.doc_query import *


def query_faq():
    with gr.Row():
        one_model_input = gr.Dropdown(label="选择OpenAI适配模型", choices=get_all_models(),
                                      value=get_selected_llm_id())

        one_model_input.change(
            use_llm,
            inputs=[one_model_input],
            outputs=[]
        )
        one_work_result_text = gr.Textbox(label="处理结果", lines=1)
    with gr.Row():
        with gr.Tab("搜索FAQ"):
            # gr.Markdown("取得匹配度最大的FAQ，使用FAQ答案进行回答。")
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        one_full_text_input_left = gr.Textbox(label="关键字(可选)", placeholder="请输入关键词",
                                                              lines=2)
                        one_question_input = gr.Textbox(label="问题（语义搜索必须）", placeholder="请输入问题",
                                                        lines=5,
                                                        value="")
                    with gr.Row():
                        one_embedding_threshold = gr.Number(label="向量检索阈值", precision=1,
                                                            value=config.get_faq_embedding_threshold)
                        one_embedding_top_k = gr.Number(label="向量检索结果个数", precision=0,
                                                        value=config.get_faq_embedding_top_k)
                        one_semantic_search_button = gr.Button("语义查询")
                    with gr.Row():
                        one_clear_question_button = gr.Button("清空问题")

                with gr.Column(scale=1):
                    with gr.Row():
                        one_query_type_right = gr.Dropdown(label="问题类别", choices=config.query_type_list,
                                                           value="ALL")
                        one_full_text_input_right = gr.Textbox(label="搜索关键字(可选)", placeholder="请输入关键词",
                                                               lines=2)
                    with gr.Row():
                        one_normal_search_button = gr.Button("普通查询")
                        one_load_all_knowledge_button = gr.Button("全部加载")

            with gr.Row():
                with gr.Column(scale=2):
                    with gr.Row():
                        one_df_output = gr.DataFrame(label="搜索结果", wrap=True, interactive=False,
                                                     headers=["ID", "问题类别", "问题"])

                    # with gr.Row():
                    # one__rerank_button = gr.Button("Rerank")
                    # one_delete_this_answer = gr.Button("删除该行")
                    # one_generate_answer_button = gr.Button("使用该行生成答案")
                    # one_generate_answer_all_button = gr.Button("使用所有行生成答案")
                    # one_generate_question_button = gr.Button("使用该答案生成问题")

                    # with gr.Row():
                    #     one_rerank_df = gr.DataFrame(label="重排序结果", wrap=True, visible=False)

                    # with gr.Row():
                    #     one_generate_result_text = gr.Textbox(label="生成结果", lines=10)

                with gr.Column(scale=1):
                    one_row_id = gr.Textbox(label="ID", lines=1, text_align="left")
                    one_row_question = gr.Textbox(label="问题", lines=3, text_align="left")
                    one_row_answer = gr.Textbox(label="答案", lines=10, text_align="left")
                    one_row_comment = gr.Textbox(label="备注", lines=1, text_align="left")
                    one_row_create_date = gr.Textbox(label="创建日期", lines=1, text_align="left")
                    one_row_filename = gr.Textbox(label="文件名", lines=1, text_align="left")

                    one_update_button = gr.Button("更新知识库")
                    one_delete_button = gr.Button("从知识库删除")
                one_clear_question_button.click(
                    clear_one_query,
                    inputs=[],
                    outputs=[one_question_input, one_full_text_input_left, one_full_text_input_right,
                             ],
                )

            # QA语义搜索
            one_semantic_search_button.click(
                one_semantic_search,
                inputs=[one_question_input, one_full_text_input_left, one_embedding_top_k,
                        one_embedding_threshold],
                outputs=[one_df_output, one_work_result_text],
            )

            # QA普通搜索
            one_normal_search_button.click(
                normal_search_knowledge,
                inputs=[one_query_type_right, one_full_text_input_right],
                outputs=[one_df_output],
            )
            # 加载所有QA
            one_load_all_knowledge_button.click(
                load_all_knowledge,
                inputs=[],
                outputs=[one_df_output],
            )

            # 点选表格
            one_df_output.select(
                fn=df_search_result_select,
                inputs=[one_df_output],
                outputs=[one_row_id, one_row_question, one_row_answer, one_row_comment, one_row_filename,
                         one_row_create_date],
            )
            # 保存知识
            one_update_button.click(
                update_one_knowledge,
                inputs=[one_row_id, one_row_question, one_row_answer, one_row_comment],
                outputs=[one_work_result_text],
            )
            # 删除知识
            one_delete_button.click(
                delete_one_knowledge,
                inputs=[one_row_id],
                outputs=[one_work_result_text],
            )
        with gr.Tab("搜索文件"):
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Row():
                            doc_one_file_left_input = gr.Dropdown(label="文件（可选）",
                                                                  choices=doc_load_filename_dropdown(), value="ALL")
                            doc_full_text_input_left = gr.Textbox(label="搜索关键字(可选)", placeholder="请输入关键词",
                                                                  lines=2)
                        with gr.Row():
                            doc_question_input = gr.Textbox(label="语义问题（语义搜索必须）", placeholder="请输入问题",
                                                            lines=3,
                                                            value="公司的工作时间是如何安排的")
                        with gr.Row():
                            doc_embedding_threshold = gr.Number(label="文档向量检索阈值", precision=1,
                                                                value=config.get_doc_embedding_threshold())
                            doc_embedding_top_k = gr.Number(label="文档向量检索结果个数", precision=0,
                                                            value=config.get_doc_embedding_top_k())
                            doc_semantic_search_button = gr.Button("语义查询")
                            # doc_split_question_button = gr.Button("问题分割")
                            # doc_recover_question_button = gr.Button("分割前问题显示")
                    with gr.Column(scale=1):
                        with gr.Row():
                            doc_one_file_right_input = gr.Dropdown(label="文件（可选）",
                                                                   choices=doc_load_filename_dropdown(), value="ALL")
                            doc_full_text_input_right = gr.Textbox(label="搜索关键字(可选)", placeholder="请输入关键词",
                                                                   lines=2)
                        with gr.Row():
                            doc_normal_search_button = gr.Button("普通查询")
                            doc_load_all_knowledge_button = gr.Button("全部加载")

                with gr.Row():
                    with gr.Column(scale=2):
                        with gr.Row():
                            doc_df_output = gr.DataFrame(label="搜索结果", wrap=True, interactive=False,
                                                         column_widths=[10, 5, 30],
                                                         headers=["ID", "文件名", "分段内容"])

                        with gr.Row():
                            doc_rerank_threshold = gr.Number(label="rerank检索阈值", precision=1,
                                                             value=config.get_rerank_threshold())
                            doc_rerank_top_k = gr.Number(label="rerank检索结果个数", precision=0,
                                                         value=config.get_rerank_top_k())
                            doc_rerank_button = gr.Button("重排序")
                        with gr.Row():
                            doc_delete_this_row = gr.Button("删除这一行")
                            doc_generate_answer_button = gr.Button("生成答案")

                        with gr.Row():
                            doc_rerank_df = gr.DataFrame(label="重排序结果", wrap=True, visible=False)

                        with gr.Row():
                            doc_generate_result_text = gr.Textbox(label="生成结果", lines=5)
                        with gr.Row():
                            with gr.Accordion(label="FAQ添加", open=False):
                                doc_faq_question_input = gr.Textbox(label="FAQ用问题", lines=2, text_align="left")
                                doc_faq_answer_input = gr.Textbox(label="FAQ用答案", lines=2, text_align="left")
                                doc_faq_comment_input = gr.Textbox(label="备注", lines=1, text_align="left")
                                doc_add_to_faq_button = gr.Button("添加到FAQ")
                                doc_add_to_faq_result_text = gr.Textbox(label="添加结果", lines=1)

                    with gr.Column(scale=1):
                        doc_row_id = gr.Textbox(label="ID", lines=1, text_align="left")
                        # doc_row_question = gr.Textbox(label="问题", lines=3, text_align="left")
                        doc_row_filename = gr.Textbox(label="文件名", lines=1, text_align="left")
                        doc_row_content = gr.Textbox(label="内容", lines=5, text_align="left")
                        # doc_row_comment = gr.Textbox(label="备注", lines=1, text_align="left")
                        doc_row_create_date = gr.Textbox(label="创建日期", lines=1, text_align="left")
                        doc_generate_question_button = gr.Button("生成问题")

                        doc_update_button = gr.Button("更新知识库")
                        doc_delete_button = gr.Button("从知识库删除")
                        doc_update_delete_result_text = gr.Textbox(label="更新结果", lines=1)

                doc_normal_search_button.click(
                    doc_normal_search_knowledge,
                    inputs=[doc_one_file_right_input, doc_full_text_input_right],
                    outputs=[doc_df_output],
                )
                doc_load_all_knowledge_button.click(
                    doc_load_all_knowledge,
                    inputs=[],
                    outputs=[doc_df_output],
                )
                doc_df_output.select(
                    fn=doc_df_search_result_select,
                    inputs=[doc_df_output],
                    outputs=[doc_row_id, doc_row_content, doc_row_filename, doc_row_create_date],
                )
                doc_semantic_search_button.click(
                    doc_semantic_search_for_ui,
                    inputs=[doc_question_input, doc_one_file_left_input,
                            doc_full_text_input_left, doc_embedding_top_k,doc_embedding_threshold],
                    outputs=[doc_df_output, one_work_result_text],
                )
                doc_delete_this_row.click(
                    doc_delete_one_search_result,
                    inputs=[doc_row_id, doc_df_output],
                    outputs=[doc_df_output, one_work_result_text],
                )
                doc_rerank_button.click(
                    doc_rerank_knowledge,
                    inputs=[doc_question_input, doc_df_output, doc_rerank_threshold, doc_rerank_top_k],
                    outputs=[doc_df_output, one_work_result_text],
                )
                doc_generate_question_button.click(
                    generate_question,
                    inputs=[doc_row_content],
                    outputs=[doc_generate_result_text],
                )
                doc_update_button.click(
                    doc_update_one_knowledge,
                    inputs=[doc_row_id, doc_row_content],
                    outputs=[doc_update_delete_result_text],
                )
                doc_delete_button.click(
                    doc_delete_one_knowledge,
                    inputs=[doc_row_id],
                    outputs=[doc_update_delete_result_text],
                )

                doc_generate_answer_button.click(
                    doc_generate_answer,
                    inputs=[doc_question_input, doc_df_output],
                    outputs=[doc_generate_result_text],
                )

                doc_add_to_faq_button.click(
                    doc_add_to_faq,
                    inputs=[doc_faq_question_input, doc_faq_answer_input, doc_faq_comment_input, doc_row_filename],
                    outputs=[doc_add_to_faq_result_text],
                )