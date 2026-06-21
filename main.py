import gradio as gr
from chat import chat

def respond(message, history):
    # Convert Gradio history (list of [user, assistant]) to OpenAI format
    formatted_history = []
    if history:
        for pair in history:
            formatted_history.append({"role": "user", "content": pair[0]})
            formatted_history.append({"role": "assistant", "content": pair[1]})

    # Call the chat function
    updated_history, image = chat(message, formatted_history)

    # Convert updated history back to Gradio format (list of [user, assistant])
    gr_history = []
    i = 0
    while i < len(updated_history):
        if (
            updated_history[i]["role"] == "user"
            and i + 1 < len(updated_history)
            and updated_history[i + 1]["role"] == "assistant"
        ):
            gr_history.append([updated_history[i]["content"], updated_history[i + 1]["content"]])
            i += 2
        else:
            i += 1  # skip malformed pair

    return "", gr_history, image  # clear input box, update chat, update image


with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(label="FlightAI Assistant", height=500)
        image_output = gr.Image(label="City Image", height=500)
    with gr.Row():
        msg = gr.Textbox(label="Ask a question", placeholder="e.g. What's the price to Tokyo?")
    with gr.Row():
        clear = gr.Button("Clear Chat")

    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot, image_output])
    clear.click(fn=lambda: ("", [], None), inputs=[], outputs=[msg, chatbot, image_output], queue=False)

ui.launch(inbrowser=True)
