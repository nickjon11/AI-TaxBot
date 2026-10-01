from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from connect import getThreadID, getConfig
from langgraphMain import getApp

#This is the main chat module. Tracks conversation history and allows for assistant and user messages

#send user message to bot
def sendMessage(message = ''):
    app = getApp()#app stores conversation history
    if(message == ''): #if the user says nothing, have the bot just introduce itself.
        message = "Introduce yourself as a tax helping chat bot."
    
    modelMessages = [HumanMessage(content=message)]#use langchain method to sent message

    #return all metadata from openAI call
    return app.invoke({"messages": modelMessages}, getConfig())

#send assistant message to bot
def sendSystemMessage(message):
    app = getApp()#app stores conversation history
    
    modelMessages = [AIMessage(content=message)]

    #return all metadata from openAI call
    return app.invoke({"messages": modelMessages}, getConfig())