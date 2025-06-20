import streamlit as st
import requests

# CONFIGURE AQUI: URL do webhook do n8n
N8N_WEBHOOK_URL = "https://n8n.diferro.com.br:5678/webhook/chat-coramdeo"

# Título e instruções
st.title("💬 Chatbot via n8n")
st.write(
    "Este chatbot usa um webhook do n8n para gerar respostas com IA. "
    "Certifique-se que o fluxo do n8n está ativo e configurado para receber mensagens no formato correto."
)

# Estado da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico da conversa
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Digite sua pergunta"):

    # Exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envia para o webhook do n8n
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"messages": st.session_state.messages},  # Envia histórico de conversa
            timeout=30
        )
        response.raise_for_status()
        ai_reply = response.json().get("reply", "❌ Resposta inválida do servidor.")
    except Exception as e:
        ai_reply = f"❌ Erro na requisição: {e}"

    # Exibe e armazena resposta
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
