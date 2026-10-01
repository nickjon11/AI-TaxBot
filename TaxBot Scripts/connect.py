from openai import OpenAI
from langchain.chat_models import init_chat_model
import random, os
from constants import getModelString as _getModelString
from constants import *

#Connect to OPENAI

#Get OpenAI api key from vault
with open(getSecretStuff(), "r") as file:
    for lines in file:
      name, value = lines.split("=")
      name = name.strip()

      if name=="api_key":
        api_key = value.strip()

#incase this is needed else where, set environment variable.
os.environ["OPENAI_API_KEY"] = api_key

#client used to send messages
client = OpenAI(
    api_key=api_key
  )

#get model string from constants, I created this before constants existed. No point in changing the implementation
def getModelString():
  return _getModelString()

#create a threadID so multiple conversations can occur at the same time. Future plans
threadID = "a" + str(random.randint(0, 9))
config = {"configurable": {"thread_id": threadID}}
model = init_chat_model(getModelString(), model_provider='openai') #langchain model

#Basic send message function with no history or rag
def sendMessage(message = '', role = 'assistant'):
  if(message == ''):
    message = "Introduce yourself as a tax helping chat bot."

  completion = client.chat.completions.create(
    model=getModelString(),
    store=True,
    messages=[{"role": role, "content": f"{message}"}]
  )

  #just return the first message
  for choice in completion.choices:
    response = choice.message
    return response.content

#langChain model will be the main way to communicate with OpenAI
def getModelObject():
  return model

#Unused
def getTokenLength():
  return 50

#return the configuration settings
def getConfig():
  return config

#Unused
def getThreadID():
  return threadID