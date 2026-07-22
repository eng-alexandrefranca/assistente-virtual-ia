import streamlit as st
import google.generativeai as genai
import os

# Configuração da página do Streamlit
st.set_page_config(page_title="DevGuide Bot", page_icon="🚀")
st.title("🚀 DevGuide Bot - Seu Tutor de Programação")
st.caption("Descubra por onde começar sua jornada na tecnologia de forma simples!")

# 1. Carregar a Base de Conhecimento e Prompt
def carregar_contexto():
    with open("data/base_conhecimento.txt", "r", encoding="utf-8") as f:
        conhecimento = f.read()
    with open("docs/prompt_sistema.md", "r", encoding="utf-8") as f:
        prompt = f.read()
    return f"{prompt}\n\n[BASE DE CONHECIMENTO]\n{conhecimento}"

contexto_sistema = carregar_contexto()

# 2. Configurar a API do Gemini (Requer chave gratuita em ai.google.dev)
# Para testar localmente, configure a variável de ambiente ou substitua temporariamente por string
API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_API_KEY_AQUI")
genai.configure(api_key=API_KEY)

# Inicializar o histórico do chat no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o DevGuide Bot. Estou aqui para te ajudar a escolher seu primeiro caminho na programação. Você tem interesse em criar interfaces de sites (Frontend), lógica dos bastidores (Backend) ou trabalhar com análise de informações (Dados)?"}
    ]

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do usuário
if user_input := st.chat_input("Digite sua dúvida aqui..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Chamar o modelo de IA passando o histórico + contexto fixo
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Construindo o prompt final contendo as regras e a pergunta do usuário
        prompt_completo = f"{contexto_sistema}\n\nHistórico da conversa:\n"
        for msg in st.session_state.messages:
            prompt_completo += f"{msg['role']}: {msg['content']}\n"
        
        response = model.generate_content(prompt_completo)
        bot_reply = response.text

        # Exibir resposta do bot
        with st.chat_message("assistant"):
            st.write(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
    except Exception as e:
        st.error("Erro ao conectar com a IA. Verifique sua API Key.")
