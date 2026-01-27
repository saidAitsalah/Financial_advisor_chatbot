import os
import sys
from dotenv import load_dotenv

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    if key in os.environ:
        del os.environ[key]

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- ENVIRONNEMENT ---
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERREUR : Clé API manquante.")
    sys.exit()

# --- 4. CONFIGURATION DU BOT ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    temperature=0.7 # Créativité (0 = robotique, 1 = poète)
)

# --- 5. CONFIGURATION DE LA MÉMOIRE ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant IA expert en finance. Tu réponds de manière concise."),
    MessagesPlaceholder(variable_name="history"), # L'historique s'insère ici
    ("human", "{input}")
])

# On crée la chaîne "intelligente"
runnable = prompt | llm

# On ajoute la gestion automatique de l'historique
# (Ceci permet de simuler une conversation continue)
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

store = {} # Stockage temporaire des conversations

chain_with_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# --- 6. TEST INTERACTIF (Console) ---
if __name__ == "__main__":
    print("🤖 BOT PRÊT ! (Tape 'quit' pour arrêter)")
    session_id = "test_user_1" # Identifiant fictif pour la session
    
    while True:
        user_input = input("\nToi : ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        response = chain_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"IA  : {response.content}")