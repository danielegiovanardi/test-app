import streamlit as st
import requests

# Configura l'URL dell'API del chatbot su n8n
N8N_CHATBOT_URL = "https://flexa.app.n8n.cloud/webhook-test/3450ada9-c5bc-4efa-8868-11c78e870f5d"  # Modifica con il tuo endpoint

st.title("Chatbot con Streamlit e n8n")

# Inizializza lo stato della chat se non è già presente
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ciao! Sono **Matteo Del Bianco**, il tuo consulente esperto in WiFi e Cambium Networks. Come posso aiutarti oggi?"}
    ]

# Mostra i messaggi della chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🌟 **Mostra i bottoni con domande suggerite se presenti**
if st.session_state.suggested_questions:
    st.write("📌 **Domande suggerite:**")
    col1, col2, col3 = st.columns(3)

    if len(st.session_state.suggested_questions) >= 1 and col1.button(st.session_state.suggested_questions[0]):
        user_input = st.session_state.suggested_questions[0]
    elif len(st.session_state.suggested_questions) >= 2 and col2.button(st.session_state.suggested_questions[1]):
        user_input = st.session_state.suggested_questions[1]
    elif len(st.session_state.suggested_questions) >= 3 and col3.button(st.session_state.suggested_questions[2]):
        user_input = st.session_state.suggested_questions[2]
    else:
        user_input = st.chat_input("Scrivi un messaggio...")
else:
    user_input = st.chat_input("Scrivi un messaggio...")
    
# **Se l'utente ha scritto o cliccato un bottone, invia il messaggio**
if user_input:
    # 1️⃣ Mostra subito il messaggio dell'utente
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2️⃣ Invio richiesta a n8n
    response = requests.post(N8N_CHATBOT_URL, json={"message": user_input})

    # 3️⃣ Recupero e visualizzazione della risposta
    if response.status_code == 200:
        response_data = response.json()

        # Estrarre la risposta principale
        bot_response = response_data[0].get("domanda1", "Errore nella risposta")

        # Estrarre le domande suggerite (le altre chiavi del JSON)
        suggested_questions = [
            response_data[0].get("domanda2", ""),
            response_data[0].get("domanda3", ""),
            response_data[0].get("domanda4", "")
        ]

        # Rimuovere eventuali stringhe vuote
        suggested_questions = [q for q in suggested_questions if q]

    else:
        bot_response = "Errore nella comunicazione con il chatbot"
        suggested_questions = []

    # 4️⃣ Mostra la risposta del chatbot
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # 5️⃣ Aggiorna le domande suggerite per la prossima interazione
    st.session_state.suggested_questions = suggested_questions
