from concurrent.futures.thread import _shutdown
import gradio as gr
import os
import PyPDF2 # type: ignore
from connect import analyze_with_gpt, cancel_shutdown, confirm_shutdown, getTokenLength, save_file, shutdownfn
from langchainMain import sendMessage
from langgraphMain import getApp
import datetime
from howtochatbot import howto_ui

#UNUSED JON CODE. USED TO INSPIRE gradioMainTaylor.py

# Initialize message history
chat_history = []

# Function to handle chatbot responses
def chatbot(user_input, history):
    history = history or []

    # Append user message
    history.append({"role": "user", "content": user_input})

    # Send to language model
    response = sendMessage(previousMessages=None, message=user_input)
    ai_response = response['messages'][-1].content
    print("sendMessage loaded:", callable(sendMessage))

    # Append AI response
    history.append({"role": "assistant", "content": ai_response}) 
    print(history)
    return "", history

# Interface layout
with gr.Blocks() as demo:
    gr.Markdown("## Omega Team – AI Taxbot")
    
    with gr.Row():
        gr.Markdown("### Navigation")
        current_page = gr.State("home")
        """
        current_page.change(render, current_page, [home_page, howtochatbot_page, account_page]) #Didn't get the multipage working properly
        with gr.Column(visible=False) as howtochatbot_page:
            howto_ui()
            gr.Button(" Back to Home").click(lambda: "home", None, current_page)
        # gr.Button("File Taxes", variant="primary")  # Placeholder
        # howto_button.click(lambda: "howtochatbot", None, current_page)
        """
       # gr.Button("Account")  Left Unused

    gr.Markdown("### Tax Filing Information")
    with gr.Row():
        for label in ["Country", "State", "Dependents", "Filing Status", "Total Income", "Total Deductions", "View Full Details"]:
            gr.Markdown(f"**{label}**") #Doesn't work

    gr.Markdown("### Suggested Questions to Ask")
    gr.Markdown("""
    1. How do I file my taxes?  
    2. What deductions am I eligible for?  
    3. How do I check my filing status?
    """)
    with gr.Row():
        with gr.Column(scale=6):
            gr.Markdown("### Chatroom")

    chatbot_output = gr.Chatbot(type='messages', label="Ask our tax chatbot stuff:")
    chatbot_input = gr.Textbox(show_label=False, placeholder="Ask our tax chatbot stuff:")
    chatbot_input.submit(chatbot, [chatbot_input, chatbot_output], [chatbot_input, chatbot_output])
    def respond(message):
        return f"You said: {message}"
    # Document Button with GPT
    with gr.Blocks() as demo2:
        gr.Markdown("# Chatbot Document Analyzer 2000")
        gr.Markdown("Upload a .txt, .pdf, or .docx document and enter a prompt (e.g., 'Read this document').")


        file_input = gr.File(label="Upload document")
        status_output = gr.Textbox(label="Status")
        file_input.change(save_file, inputs=file_input, outputs=status_output)
        # gr.Button("Close Chatbot").click(shutdownfn)
        shutdownfn_button = gr.Button("Close Chatbot")
        with gr.Row(visible=False) as confirm_panel:
            gr.Markdown("Are you sure you want to close the chatroom?")
            confirm = gr.Button("Yes")
            cancel = gr.Button("Cancel")
        shutdownfn_button.click(fn=confirm_shutdown, outputs=confirm_panel)
        cancel.click(fn=cancel_shutdown, outputs=confirm_panel)
        confirm.click(fn=shutdownfn)

# Dev Testing OpenAI reading documents here (Take a look and modify this code)
    #with gr.Row():
    #    file_input = gr.File(label="Upload Document")
    #    prompt_input = gr.Textbox(lines=2, placeholder="Ask something about the document (e.g. summarize it)", label="Prompt")
    #output = gr.Textbox(label="gpt-4o-mini Response", lines=15)

    #submit_button = gr.Button("Anaylze")
    #submit_button.click(analyze_with_gpt, inputs=[file_input, prompt_input], outputs=output)                        
                                  
demo.launch(share=True)