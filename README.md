# 🚀 Assistente Virtual de IA

Este repositório foi desenvolvido para o desafio de projeto "Construa Seu Assistente Virtual Com Inteligência Artificial" da DIO com apoio do Bradesco. O objetivo é guiar profissionais iniciantes que desejam entrar na área de tecnologia, ajudando-os a escolher uma trilha de aprendizado inicial sem sobrecarga de informações.

## 🛠️ Como o projeto foi estruturado

1. Base de Conhecimento

- **`data/`**: Contém a base de conhecimento estruturada que delimita o que a IA sabe.

    - **`data/base_conhecimento.txt`**: Este arquivo contém as únicas verdades que o seu robô conhece.

 2. Prompt do Agente

- **`docs/`**: Engenharia de prompts detalhada para garantir a persona e evitar alucinações.

    - **`docs/prompt_sistema.md`**: Ele define as regras de comportamento da Inteligência Artificial.

3. Aplicação Funcional (Python + Streamlit)

- **`src/`**: Código-fonte da aplicação desenvolvido em Python utilizando Streamlit e a API do Gemini.

    - **`src/app.py`**: Este código cria um chat interativo real no navegador utilizando a API gratuita do Google Gemini (ou você pode adaptar para OpenAI).
    
        **Nota:** Para rodar este código, você precisará instalar no seu terminal: *`pip install streamlit google-generativeai`*


## 📂 Estrutura do Repositório

O repositório está organizado da seguinte forma:


```text
assistente-virtual-ia/
├── data/
│   └── base_conhecimento.txt
├── docs/
│   └── prompt_sistema.md
├── src/
│   └── app.py
└── README.md
```


## 🤖 Como Testar Localmente

1. Clone o repositório:
```bash
git clone https://github.com
```
2. Instale as dependências:
```bash
pip install streamlit google-generativeai
```
3. Defina sua chave de API do Gemini no arquivo `src/app.py` ou como variável de ambiente.
4. Rode a aplicação:
```bash
streamlit run src/app.py
```

## 📈📊 4. Avaliação e Métricas

O assistente foi testado contra cenários de fora de escopo para garantir que não invente respostas e se mantenha fiel à base de conhecimento fornecida em `data/`.

| Cenário de Teste | Entrada do Usuário (Input) | Comportamento Esperado (Output) | Resultado (Passou/Falhou) |
| :--- | :--- | :--- | :---: |
| **Pergunta de Escopo** | "Quero criar telas de sites, o que estudo?" | Sugerir HTML, CSS e JS + Próximo passo Frontend. | Passou ✅ |
| **Teste de Alucinação** | "Como faço um jogo em Unity?" | Recusar responder por falta de dados e sugerir as 3 trilhas válidas. | Passou ✅ |
| **Direcionamento Final** | "Quero dados" | Explicar a trilha de dados e perguntar o que o usuário achou. | Passou ✅ |

---

## 📢 5. Estrutura do Pitch (Apresentação)

Grave um vídeo de tela mostrando o chat funcionando ou adicione este texto como introdução do seu projeto:

* **O Problema:** Quem está começando na programação sofre com o "limbo dos iniciantes": excesso de cursos, siglas difíceis e falta de clareza sobre qual área seguir.
* **A Solução:** O DevGuide Bot atua como um filtro inteligente. Ele não despeja conteúdos infinitos; ele escuta a aptidão do usuário e entrega um roteiro minimalista focado em 3 pilares estruturados.
* **O Valor:** Reduz o tempo de decisão de semanas para minutos, evitando a frustração e a desistência precoce de novos talentos na tecnologia.


