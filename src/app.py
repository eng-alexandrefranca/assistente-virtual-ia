import streamlit as st
import google.generativeai as genai
import os
import io
from dotenv import load_dotenv
from gtts import gTTS
from rag_engine import buscar_contexto_relevante
from prompts import carregar_system_prompt, formatar_prompt_final

# 1. Carregar variáveis do arquivo .env automaticamente
load_dotenv()

# Configuração da página Streamlit
st.set_page_config(page_title="Guia de Acessibilidade", page_icon="♿", layout="centered")

st.title("♿ Guia de Acessibilidade")
st.caption("Pré-atendimento empático por Texto e Voz, com direcionamento especializado.")

# Configurar API Key (suporta tanto GEMINI_API_KEY quanto GOOGLE_API_KEY)
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")

if not API_KEY:
    st.warning("⚠️ Variável GEMINI_API_KEY ou GOOGLE_API_KEY não configurada no arquivo .env.")

genai.configure(api_key=API_KEY)

# Função para converter texto da resposta em áudio (Text-to-Speech)
def gerar_audio_resposta(texto: str) -> bytes:
    try:
        tts = gTTS(text=texto, lang='pt', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        print(f"Erro ao gerar áudio TTS: {e}")
        return None

# Inicializar Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá. Sou o Guia de Acessibilidade. Como posso te ajudar hoje?"}
    ]

# Carregar Prompt de Sistema
system_prompt = carregar_system_prompt()

# Gravação por Voz NATIVA do Streamlit
audio_gravado = st.audio_input("🎙️ Enviar mensagem por Voz (Microfone):")

# Exibir histórico de mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "audio" in message and message["audio"]:
            st.audio(message["audio"], format="audio/mp3")

user_input = None
audio_bytes = None

# Capturar gravação nativa do Streamlit
if audio_gravado:
    audio_bytes = audio_gravado.read()
    user_input = "Mensagem de voz enviada pelo usuário."

# Capturar mensagem de texto se o usuário digitar
text_input = st.chat_input("Ou digite sua dúvida por texto...")
if text_input:
    user_input = text_input
    audio_bytes = None

# Processamento da Mensagem
if user_input:
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
            
            if audio_bytes:
                conteudo_gemini = [
                    prompt_completo,
                    {"mime_type": "audio/wav", "data": audio_bytes}
                ]
                response = model.generate_content(conteudo_gemini)
            else:
                response = model.generate_content(prompt_completo)

            bot_reply = response.text
            st.write(bot_reply)

            # Gerar sintese de voz (áudio) da resposta
            bot_audio = gerar_audio_resposta(bot_reply)
            if bot_audio:
                st.audio(bot_audio, format="audio/mp3", autoplay=True)

            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_reply,
                "audio": bot_audio
            })
        except Exception as e:
            st.error("Erro ao processar mensagem. Verifique a chave de API no arquivo .env.")
            st.caption(f"Detalhes: {e}")
