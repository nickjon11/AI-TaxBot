from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from connect import getModelObject

#create StateGraph app to store messages

model = getModelObject() #main chat langchain model  

mainWorkFlow = StateGraph(state_schema=MessagesState)

#send message to LLM 
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

mainWorkFlow.add_edge(START, "model")
mainWorkFlow.add_node("model", call_model)

memory = MemorySaver()
app = mainWorkFlow.compile(checkpointer=memory)

#main conversation object.
def getApp():
    return app
