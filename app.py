import streamlit as st
import os
import sys
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    if key in os.environ:
        del os.environ[key]

st.set_page_config(page_title="Chatbot financial advisor", page_icon="🤖")
st.title("🤖 Assistant IA - financial")

load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Clé API manquante. Vérifie ton fichier .env")
    st.stop()

with st.sidebar:
    st.header("⚙️ Configuration")
    model_choice = st.selectbox(
        "Modèle", 
        ["gemini-pro", "gemini-2.5-flash-lite"], 
        index=0
    )
    
    system_prompt = st.text_area(
        "Personnalité du chatbot :",
        "Tu es un assistant IA expert en finance. Tu réponds de manière concise.",
        help="Changez ici le rôle de l'IA (ex: Expert Finance, Coach Sportif...)"
    )
    
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.chat_history = []
        st.rerun()

llm = ChatGoogleGenerativeAI(
    model=model_choice,
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

user_input = st.chat_input("Votre message ici...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt), # La personnalité définie dans la sidebar
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt_template | llm

    with st.chat_message("assistant"):
        with st.spinner("L'IA réfléchit..."):
            try:
                response = chain.invoke({
                    "history": st.session_state.chat_history[:-1], 
                    "input": user_input
                })
                st.markdown(response.content)
                
                st.session_state.chat_history.append(AIMessage(content=response.content))
                
            except Exception as e:
                st.error(f"Erreur API : {e}")