import gradio as gr
from langchainMain import sendMessage, sendSystemMessage
from fileManagement import process_file, shutdownfn
from constants import *
from pineconeSearch import pineconeQuickSearch

"""
This is the main file to run. It uses all other methods to build a gradio interface for the users.
RUN THIS TO CREATE GRADIO LINK both localhost on server hosted.
"""


# Initialize message history
chat_history = []

# Function to handle chatbot responses
firstRun = True
def chatbot(user_input, history):
    global firstRun
    global chat_history
    chat_history = history or []
    
    #if it is the first time the bot is being launched set the conversation parameters.
    if firstRun:
        sendSystemMessage(getFirstMessage())
        firstRun=False #only send first message once

    pineconeSearchResults = pineconeQuickSearch(user_input) #use quick search function to check if RAG would be helpful
    
    #If there is a response, RAG is helpful. Get the chunk data and send it to the bot
    if(pineconeSearchResults):
        rag = '\n\n'.join(pineconeSearchResults)
        sendSystemMessage("This is RAG information you can use in your next answer:\n" + rag)
    
    # Append user message
    chat_history.append({"role": "user", "content": user_input})

    # Send to language model
    response = sendMessage(message=user_input)
    ai_response = response['messages'][-1].content

    # Append AI response
    chat_history.append({"role": "assistant", "content": ai_response}) 
    return "", chat_history

#UNUSED
def getHistory():
    global chat_history
    return chat_history


#Create Gradio interface

# Interface layout
with gr.Blocks() as demo:
    #Set CSS values to minorly adjust elements
    gr.HTML("""
    <style>
            #chatbot-send-btn{
                height: 100% !important;
                padding-top: 20px;
                padding-bottom: 20px;
            }
    </style>  
    """)

    #Write down the title of the webpage
    gr.Markdown("## Omega Team – AI Taxbot")
    
    #create a row of Naviagation options
    with gr.Row():
        gr.Markdown("### Navigation")
        gr.Button("File Taxes", variant="primary", scale=2)  # Placeholder
        gr.Button("Close Chatbot", scale=1).click(shutdownfn)


    #Write down suggested questions
    gr.Markdown("### Suggested Questions to Ask")
    gr.Markdown("""
    1. How do I file my taxes?&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. What deductions am I eligible for?&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. How do I check my filing status?
    """)

    #default declaration
    send_btn = None
    file = None
    
    #Skip some area
    with gr.Row():
        gr.Markdown("\n\n")
    
    #Create area to upload documents
    with gr.Row():
        with gr.Column(scale=1):
            file = gr.File(label="Upload W2", file_types=[".txt", ".pdf", ".docx"], height=40)
            send_btn = gr.Button("Process W2")
        with gr.Column(scale=20):
            gr.Markdown(" ")
            
    #create chat output area
    chatbot_output = gr.Chatbot(type='messages', label="Ask our tax chatbot stuff:")

    #add an input text are and submit button. Place on same row
    with gr.Row():
        chatbot_input  = gr.Textbox(show_label=False, placeholder="Ask our tax chatbot stuff:", scale=20)
        submitButton = gr.Button("Send", size="md",elem_id='chatbot-send-btn')#add element id to allow CSS editing

    #Set input area enter press and submit button click to show output and clear the input box
    chatbot_input.submit(chatbot, [chatbot_input, chatbot_output], [chatbot_input, chatbot_output])
    submitButton.click(chatbot, [chatbot_input, chatbot_output], [chatbot_input, chatbot_output])

    #When the Document Process button is clicked call the handler with the W2 prompt
    PROMPT = getW2Prompt() #from constants
    if(send_btn and file):
        prompt = gr.State(PROMPT)
        send_btn.click(
            fn= process_file,
            inputs=[file,prompt],
            show_progress_on=file
        )

#Launch this file to create gradio interface.
if __name__ == "__main__":
    demo.launch(share=True)