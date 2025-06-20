import streamlit as st
import requests
import uuid
import urllib3

# Desativa avisos de SSL (somente para testes — NÃO use verify=False em produção)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL do webhook do n8n compatível com @n8n/chat
CHAT_URL = "https://n8n.diferro.com.br:5678/webhook-test/834f1870-5d63-4dcb-a31f-a4d69b4200bb"  # 🔁 Substitua pelo seu webhook real

st.set_page_config(page_title="Chat Coram Deo", page_icon="💬")
st.title("💬 Chat com a IA via n8n/chat")

# ID de sessão único por usuário
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Digite sua pergunta"):

    # Exibe e salva a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara payload no formato do n8n/chat
    payload = {
        "chatInput": prompt,
        "sessionId": st.session_state.session_id,
        "action": "input"
    }

    try:
        response = requests.post(CHAT_URL, json=payload, verify=False)
        response.raise_for_status()
        data = response.json()

        # Extrai a resposta da IA
        resposta = data["answers"][0]["message"] if "answers" in data else "⚠️ Resposta não encontrada."

    except Exception as e:
        resposta = f"❌ Erro: {e}"

    # Exibe e salva a resposta da IA
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
