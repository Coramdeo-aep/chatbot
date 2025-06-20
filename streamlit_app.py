import streamlit as st
import requests
import uuid
import urllib3

# Desativa aviso de SSL (apenas para testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL do webhook configurado com $json.chatInput
CHAT_URL = "https://n8n.diferro.com.br:5678/webhook/0731a047-3e95-4a35-8a56-d8e9f999ed5c/chat"  # <-- atualize esse link

# Sessão única de chat por usuário
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 Chat com a IA via n8n/chat")

# Exibe histórico de mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envia para n8n no formato chatInput
    try:
        payload = {
            "chatId": st.session_state.chat_id,
            "chatInput": prompt
        }

        response = requests.post(CHAT_URL, json=payload, verify=False)
        response.raise_for_status()

        resposta = response.json()["answers"][0]["message"]

    except Exception as e:
        resposta = f"❌ Erro: {e}"

    # Mostra e armazena a resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
