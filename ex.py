import os
import streamlit as st
import openai

# Définir la clé API OpenAI
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]

# Fonction pour générer une réponse avec OpenAI
def generate_response(prompt):
    """Utilise l'API OpenAI pour générer une réponse basée sur un prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Vous pouvez remplacer par "gpt-3.5-turbo" si nécessaire
            messages=[
                {"role": "system", "content": "Tu es un expert en football et en statistiques."},
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Erreur lors de la génération de la réponse : {e}"

# Interface Streamlit
st.title("Assistant Ballon d'Or avec OpenAI")
st.markdown("Posez vos questions sur le Ballon d'Or et obtenez des réponses intelligentes grâce à OpenAI !")

# Entrée de question
prompt = st.text_area(
    "Posez votre question :",
    placeholder="Exemple : Qui sont les nominés pour le Ballon d'Or 2023 ? Quelles sont les statistiques de Lionel Messi cette saison ?",
)

# Actions
if st.button("Obtenir une réponse"):
    if prompt:
        # Génération de réponse avec OpenAI
        answer = generate_response(prompt)

        # Affichage de la réponse
        st.markdown(f"**Réponse :** {answer}")
    else:
        st.error("Veuillez entrer une question avant de cliquer sur le bouton.")
