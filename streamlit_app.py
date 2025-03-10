import streamlit as st
import requests

# Configura l'URL dell'API del chatbot su n8n
N8N_CHATBOT_URL = "https://flexa.app.n8n.cloud/webhook/3450ada9-c5bc-4efa-8868-11c78e870f5d"  # Modifica con il tuo endpoint

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

# 🌟 **Bottoni per domande suggerite**
st.write("📌 **Domande suggerite:**")
col1, col2, col3 = st.columns(3)

if col1.button("Quale Access Point Cambium fa al caso mio?"):
    user_input = "Quale Access Point Cambium fa al caso mio?"

elif col2.button("Qual è la differenza tra i modelli Cambium?"):
    user_input = "Qual è la differenza tra i modelli Cambium?"

elif col3.button("Come configurare un AP Cambium Networks?"):
    user_input = "Come configurare un AP Cambium Networks?"

else:
    user_input = st.chat_input("Scrivi un messaggio...")
    
# Input dell'utente
if user_input:
    # 1️⃣ Mostra subito il messaggio dell'utente
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # **2. Invio richiesta a n8n**
    response = requests.post(N8N_CHATBOT_URL, json={"message": user_input})

    # **3. Recupero e visualizzazione della risposta**
    if response.status_code == 200:
        bot_response = response.json().get("output", "Errore nella risposta")
    else:
        bot_response = "Errore nella comunicazione con il chatbot"

    # **4. Aggiorna lo stato con la risposta**
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
