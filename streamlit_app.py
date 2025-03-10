import streamlit as st
import requests

# Configura l'URL dell'API del chatbot su n8n
N8N_CHATBOT_URL = "https://flexa.app.n8n.cloud/webhook-test/4f82f77e-623f-4463-8284-db7ddeb33e0c"  # Modifica con il tuo endpoint

st.title("Chatbot con Streamlit e n8n")

# Inizializza lo stato della chat se non è già presente
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi della chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
user_input = st.chat_input("Scrivi un messaggio...")

if user_input:
    # Aggiungi il messaggio dell'utente allo stato della chat
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Invia il messaggio all'API di n8n
    response = requests.post(N8N_CHATBOT_URL, json={"message": user_input})

    if response.status_code == 200:
        bot_response = response.json().get("reply", "Errore nella risposta")
    else:
        bot_response = "Errore nella comunicazione con il chatbot"

    # Aggiungi la risposta del bot allo stato della chat
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Mostra il messaggio del bot
    with st.chat_message("assistant"):
        st.markdown(bot_response)
