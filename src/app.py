import streamlit as st
import google.generativeai as genai
import os
from rag_engine import buscar_contexto_relevante
from prompts import carregar_system_prompt, formatar_prompt_final

# Configuração da página Streamlit
st.set_page_config(page_title="Guia de Acessibilidade", page_icon="♿", layout="centered")

st.title("♿ Guia de Acessibilidade")
st.caption("Pré-atendimento empático e direcionamento para equipes especializadas.")

# Configurar API Key
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    st.warning("⚠️ Variável GEMINI_API_KEY não configurada. Configure no ambiente ou no arquivo .env.")

genai.configure(api_key=API_KEY)

# Inicializar Histórico do Chat com a nova persona
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá. Sou o Guia de Acessibilidade. Como posso te ajudar hoje?"}
    ]

# Carregar Prompt de Sistema
system_prompt = carregar_system_prompt()

# Exibir Mensagens Anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Entrada do Usuário
if user_input := st.chat_input("Digite sua mensagem aqui..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 1. Recuperar contexto da base de conhecimento (RAG)
    contexto = buscar_contexto_relevante(user_input)

    # 2. Formatar histórico recente
    historico_texto = ""
    for msg in st.session_state.messages[-6:]:
        historico_texto += f"{msg['role']}: {msg['content']}\n"

    # 3. Montar prompt completo
    prompt_completo = formatar_prompt_final(system_prompt, contexto, historico_texto, user_input)

    # 4. Gerar Resposta via Gemini API
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt_completo)
            bot_reply = response.text
            st.write(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
            msg_erro = "Desculpe, ocorreu um erro ao conectar com a IA."
            st.error(msg_erro)
            st.caption(f"Detalhes: {e}")
