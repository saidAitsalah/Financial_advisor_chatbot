import os
import google.generativeai as genai
from dotenv import load_dotenv

for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    if key in os.environ:
        del os.environ[key]

#Config
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("📋 Recherche des modèles disponibles pour ta clé...")

try:
    models = genai.list_models()
    
    found_any = False
    print("\n✅ MODÈLES DISPONIBLES :")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
            found_any = True
            
    if not found_any:
        print("❌ Aucun modèle de génération de texte trouvé.")
        
except Exception as e:
    print(f"❌ Erreur : {e}")