import gradio as gr

#UNUSED Future implementation of training method.

# Interface layout
with gr.Blocks() as demo:
    gr.Markdown("## Omega Team – AI Taxbot")
    
    with gr.Row():
        gr.Markdown("### Navigation")
        gr.Button("File Taxes", variant="primary")  # Placeholder
        gr.Button("How to use Chatbot") # Placeholder
        gr.Button("Account")  # Placeholder

def howto_ui():
    with gr.Box():
        gr.Markdown("""

** Welcome to the Chatbot for Tax Forms! This is how to use it: **
     1. **Type Your Question**: In the input box, ask your tax-related question.
        2. **Wait for Response**: The chatbot will process and give you a helpful reply.
        3. **Upload Documents (if supported)**: You can upload relevant files for better assistance.
        4. **Review and Clarify**: Ask follow-up questions if needed.

        **Example Questions:**
        - "How do I file a W-2?"
        - "What documents do I need for a 1099?"
        - "Can you help me understand my tax bracket?"

        We're here to help simplify your tax process!                         
                    """)
        