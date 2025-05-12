import gradio as gr

def greet_trae(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet_trae, inputs="text", outputs="text")
demo.launch()