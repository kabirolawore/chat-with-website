import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


def get_response(user_input):
    return "You said"


# app config
st.set_page_config(
    page_title="Chat with websites",
    page_icon="👋",
)
st.title("Chat with websites")

# Persist the chat history after every streamlit rerun
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot, how can I help you?"),
    ]



# User input
user_query = st.chat_input("Ask a question about the  website")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=get_response(user_query)))
    # with st.chat_message("Human"):
    #     st.write(user_query)
    # response = get_response(user_query)
    # with st.chat_message("AI"):
    #     st.write(response)


# with st.chat_message("Human"):
#     st.write("I want to know about the weather in New York")

# Sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")
    st.write(website_url)
    st.write(st.session_state.chat_history)

# Conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)