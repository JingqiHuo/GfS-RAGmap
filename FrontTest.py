import gradio as gr
from main import processing


with gr.Blocks() as demo:

    # Gradio frontend component
    gr.Markdown("Demo")
    user_input = gr.Textbox(label="Please enter your question")
    btn = gr.Button("Submit")
    output_text = gr.Textbox(label="Answer")
    output_map = gr.HTML(label="Map Display")

    btn.click(fn=processing, inputs=user_input, outputs=[output_text, output_map])

demo.launch(share=True)


    