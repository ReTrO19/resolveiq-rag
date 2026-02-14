from dotenv import load_dotenv
from core import main_runner
import gradio as gr
import os



def format_context(context):
    result = f"<h2 style='color: #ff7800;'>Relevent Context</h2>\n\n"
    for doc in context:
        result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
        result += doc.page_content + "\n\n"
    return result

def chat(history):
    print("History :", history)
    last_message = history[-1]["content"][0]["text"]
    prior = history[:-1]
    print("Last Message :", last_message)
    print("Prior Message :", prior)

    answer, context = main_runner(last_message, prior)
    history.append({"role":"assistant", "content":answer})
    return history, format_context(context)

def main():
    load_dotenv(override=True)

    def put_message_in_chatbot(message, history):
        return "", history + [{"role": "user", "content":message}]
    
    theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serf"])

    with gr.Blocks(title="ResolveIQ 🧠", theme=theme) as ui:
        gr.Markdown("# ResolveIQ 🧠\n Ask me anything about Projects!")

        with gr.Row():
            with gr.Column(scale=1):
                chatbot = gr.Chatbot(
                    label="Conversation", height=600,
                )

                message = gr.Textbox(
                    label= "Your Question",
                    placeholder= "Ask anything about Project ..",
                    show_label=True
                )
            
            with gr.Column(scale=1):
                context_markdown = gr.Markdown(
                    label="Retrival Context",
                    value="Retrieved context will appear here",
                    container=True,
                    height=600
                )
        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_markdown])
    ui.launch(inbrowser=True)

if __name__ == "__main__":
    main()