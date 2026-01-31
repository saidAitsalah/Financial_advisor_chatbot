# Agent Conseiller Financier

## Description
Ce projet, développé implémente un agent conversationnel spécialisé dans le conseil financier. L'application exploite LLM gemini-pro pour fournir des explications pédagogiques sur des concepts financiers, des stratégies d'investissement et la gestion des risques pour débutants.

## Acces au chatbot déployé :  https://financialadvisorchatbot-jx2exutabvheebqp2cpjqj.streamlit.app/


## Architecture Technique

L'application est construite sur la pile technologique suivante :

* **LLM :** gemini-2.5-flash-lite .
* **Orchestration :** LangChain.
* **Interface Utilisateur :** Streamlit.
* **Monitoring :** LangSmith.

## Installation

### Prérequis
* Python 3.9 ou version supérieure.
* Une clé API Google Cloud avec accès aux modèles LLM.
* (Optionnel) Une clé API LangSmith pour le monitoring.

### Configuration Locale

1.  **Cloner le dépôt :**
    ```bash
    git clone <url_du_depot>
    cd Financial_advisor_chatbot
    ```

2.  **Créer et activer un environnement virtuel :**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/MacOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration des variables d'environnement :**
    Créer un fichier `.env` à la racine du projet et définir les variables suivantes :
    ```ini
    GOOGLE_API_KEY=votre_cle_api_google_ici
    
    # Optionnel : Pour le monitoring LangSmith
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=[https://api.smith.langchain.com](https://api.smith.langchain.com)
    LANGCHAIN_API_KEY=votre_cle_api_langsmith_ici
    LANGCHAIN_PROJECT=Chatbot_Finance_UTT
    ```

## Utilisation

Pour lancer l'application en local, exécuter la commande suivante :

```bash
streamlit run app.py
