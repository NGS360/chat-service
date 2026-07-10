
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

def chat_node(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()

