import streamlit as st
# from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def get_response(user_input):
    return "You said"


def get_vectorstore_from_url(url):
    # get the text in document form
    loader = WebBaseLoader(url)
    doc = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    doc_chunks = text_splitter.split_documents(doc)

    # create a vector store from the chunks
    vector_store = Chroma.from_documents(
        doc_chunks,
        embedding=OpenAIEmbeddings()
    )

    return vector_store


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


# Sidebar
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL")
    st.write(website_url)
    st.write(st.session_state.chat_history)

if not website_url:
    st.info("Please enter a website url")
else:
    document_chunks = get_vectorstore_from_url(website_url)
    with st.sidebar:
        st.write(document_chunks)

    # User input
    user_query = st.chat_input("Ask a question about the  website")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=get_response(user_query)))
        # with st.spinner("Thinking..."):
        #     st.write(get_response(user_query))


# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)