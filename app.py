import streamlit as st
import os
import sys
import base64
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from PIL import Image

# CONFIG RÉSEAU 
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    if key in os.environ:
        del os.environ[key]

st.set_page_config(page_title="Chatbot Financial Advisor", page_icon="💰")
st.title("Assistant IA - Finance")


load_dotenv()
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Clé API manquante. Vérifie ton fichier .env")
    st.stop()


with st.sidebar:
    st.header(" Configuration")
    
   
    model_choice = st.selectbox(
        "Modèle", 
        ["gemini-2.5-flash-lite"], 
        index=0
    )
    
    st.divider()
    
    st.write("📷 Analyse de document")
    img_file = st.file_uploader("Envoyer un graphique/chart", type=["png", "jpg", "jpeg"])
    
    default_prompt = """Tu es un Conseiller Financier Senior expérimenté et prudent.
    Tes réponses doivent être :
    1. Pédagogiques (explique les termes complexes comme ETF, PEA, Crypto).
    2. Prudentes (ajoute toujours un avertissement : "Ceci n'est pas un conseil en investissement certifié").
    3. Structurées (utilise des listes à puces).

    Si on te pose une question hors de la finance , réponds poliment que tu ne traites que les sujets financiers."""
    
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

user_input = st.chat_input("Votre question financière...")

if user_input:
   
    with st.chat_message("user"):
        st.markdown(user_input)
        if img_file:
            st.image(img_file, caption="Image envoyée", use_column_width=True)

    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("assistant"):
        with st.spinner("L'IA analyse..."):
            try:
                if img_file:
                    
                    img_bytes = img_file.getvalue()
                   
                    base64_image = base64.b64encode(img_bytes).decode('utf-8')
                    # format attendu par LangChain Data URI
                    image_data = f"data:{img_file.type};base64,{base64_image}"

                    response = llm.invoke([
                        HumanMessage(content=[
                            {"type": "text", "text": default_prompt + "\n\nAnalyse cette image et réponds à : " + user_input},
                            {"type": "image_url", "image_url": image_data} 
                        ])
                    ])
                
                # Texte seul
                else:
                    prompt_template = ChatPromptTemplate.from_messages([
                        ("system", default_prompt),
                        MessagesPlaceholder(variable_name="history"),
                        ("human", "{input}")
                    ])
                    chain = prompt_template | llm
                    
                    response = chain.invoke({
                        "history": st.session_state.chat_history[:-1], 
                        "input": user_input
                    })

                # Affichage et sauvegarde réponse
                st.markdown(response.content)
                st.session_state.chat_history.append(AIMessage(content=response.content))
                
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")