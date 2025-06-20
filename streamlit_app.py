import streamlit as st
import requests
import uuid
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL do endpoint do agente de chat
CHAT_ENDPOINT = "https://n8n.diferro.com.br:5678/webhook/0731a047-3e95-4a35-8a56-d8e9f999ed5c/chat"  # atualize o ID

# Inicializa sessão única de chat
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())  # gera um ID único

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💬 Chat com a IA (estilo n8n/chat)")

# Mostra histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Digite sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "chat_id": st.session_state.chat_id,
            "message": prompt
        }
        response = requests.post(CHAT_ENDPOINT, json=payload, verify=False)
        response.raise_for_status()

        resposta = response.json()["answers"][0]["message"]  # padrão do n8n/chat

    except Exception as e:
        resposta = f"❌ Erro: {e}"

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
