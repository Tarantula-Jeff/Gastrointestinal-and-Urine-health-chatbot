import os
import streamlit as st

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import css, bot_template, user_template


def get_pdf_text():
    fixed_pdf_path = "FeedDocs/Urine and poop health4.pdf"
    text = ""

    pdf_reader = PdfReader(fixed_pdf_path)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )

    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain


def handle_userinput(user_question):
    if "conversation" not in st.session_state:
        raw_text = get_pdf_text()
        text_chunks = get_text_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks)

        st.session_state.conversation = get_conversation_chain(
            vectorstore
        )

    response = st.session_state.conversation.invoke(
        {"question": user_question}
    )

    st.session_state.chat_history = response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace(
                    "{{MSG}}",
                    message.content
                ),
                unsafe_allow_html=True
            )
        else:
            st.write(
                bot_template.replace(
                    "{{MSG}}",
                    message.content
                ),
                unsafe_allow_html=True
            )


def main():
    load_dotenv()

    st.set_page_config(
        page_title="Sturine Chatbot",
        page_icon="🤖"
    )

    st.write(css, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Sturine Chatbot 🤖")

    user_question = st.text_input(
        "Ask a question concerning your gut and urinary health:"
    )

    if user_question:
        handle_userinput(user_question)


if __name__ == "__main__":
    main()
