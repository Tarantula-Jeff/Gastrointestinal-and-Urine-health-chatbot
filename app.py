import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from htmlTemplates import css, bot_template, user_template


def get_pdf_text():
    fixed_pdf_path = "C:\\Users\\jeffr\\Desktop\\SturineChat\\FeedDocs\\Urine and poop health.pdf"
    text = ""
    pdf_reader = PdfReader(fixed_pdf_path)
    for page in pdf_reader.pages:
            text += page.extract_text()
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
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
      if "conversation" not in st.session_state:
        # Process PDF and create conversation chain
        raw_text = get_pdf_text()
        text_chunks = get_text_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks)
        st.session_state.conversation = get_conversation_chain(vectorstore)

      response = st.session_state.conversation({'question': user_question})
      st.session_state.chat_history = response['chat_history']
      for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)



def main():
    load_dotenv()
    st.set_page_config(page_title="Sturine Chatbot", page_icon=":robot_face:")
    st.write(css, unsafe_allow_html=True)

    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Sturine Chatbot :robot_face:")
    user_question=st.text_input("Ask question concerning your guts and urine health:")
    if user_question:
         handle_userinput(user_question)


    


                
if __name__ == '__main__':
    main() 