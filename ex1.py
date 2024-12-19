import os
import requests
import streamlit as st
import google.generativeai as genai

# Définir les variables d'environnement pour les clés API
os.environ["GEMINI_API_KEY"] = "AIzaSyCqozHPzc1NRb-Xf4t6DEYTDIutFcOe_bU"
os.environ["FOOTBALL_API_KEY"] = "f50308e571124a3393a11df1307c789e"

# Configurer l'API Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# URL et en-têtes pour l'API de football
FOOTBALL_API_URL = "https://api.football-data.org/v4/players"
headers = {
    "X-RapidAPI-Host": "api.football-data.org",
    "X-RapidAPI-Key": os.environ["FOOTBALL_API_KEY"],
}

# Fonction pour récupérer les données des joueurs
def get_player_stats(player_name):
    """Recherche les statistiques d'un joueur via une API de football."""
    params = {"search": player_name, "season": "2023"}
    response = requests.get(FOOTBALL_API_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["response"]:
            return data["response"][0]  # Retourne les données du premier résultat
        else:
            return {"error": "Aucune donnée trouvée pour ce joueur."}
    else:
        return {"error": f"Erreur lors de la récupération des données : {response.status_code}"}

# Fonction pour générer une réponse avec Gemini
def generate_response(prompt):
    """Utilise Gemini pour générer des réponses basées sur un prompt."""
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Interface Streamlit
st.title("LLM sur les nominés au Ballon d'Or")
st.markdown("Posez vos questions sur n'importe quel joueur et obtenez des réponses intelligentes !")

# Entrée du nom du joueur
player_name = st.text_input("Entrez le nom d'un joueur :", placeholder="Exemple : Lionel Messi")

# Entrée de question
question = st.text_input("Posez une question :", placeholder="Exemple : Quelles sont ses statistiques cette saison ?")

# Actions
if st.button("Obtenir une réponse"):
    if player_name and question:
        # Récupération des données du joueur
        stats = get_player_stats(player_name)
        if "error" in stats:
            st.error(stats["error"])
        else:
            # Construction du prompt
            prompt = f"Voici les données disponibles pour {player_name} : {stats}. Maintenant, réponds à la question : {question}"

            # Génération de réponse avec Gemini
            answer = generate_response(prompt)

            # Affichage de la réponse
            st.markdown(f"**Réponse :** {answer}")
    else:
        st.error("Veuillez entrer un nom de joueur et poser une question.")