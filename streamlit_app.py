import streamlit as st
import requests
import urllib3

# Desativa warnings de SSL inseguros (somente para testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL do webhook do n8n
WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook-test/chat-coramdeo"

st.title("💬 Chat com a IA via n8n")

# Inicializa o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de conversa
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada de mensagem
if prompt := st.chat_input("Digite sua pergunta"):

    # Adiciona pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Envia apenas a última pergunta para o webhook, no formato esperado: {"pergunta": ...}
        response = requests.post(WEBHOOK_URL, json={"pergunta": prompt}, verify=False)
        response.raise_for_status()
        resposta = response.json().get("resposta", "⚠️ Resposta não encontrada.")

    except Exception as e:
        resposta = f"❌ Erro na requisição: {e}"

    # Exibe e armazena resposta da IA
    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
