import os

def carregar_system_prompt(path: str = "docs/prompt_sistema.md") -> str:
    """Carrega o System Prompt das regras de comportamento do agente."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Você é um assistente de acessibilidade prestativo."

def formatar_prompt_final(system_prompt: str, contexto: str, historia: str, pergunta: str) -> str:
    """Combina o System Prompt, contexto recuperado do RAG e histórico da conversa."""
    return f"""{system_prompt}

=== BASE DE CONHECIMENTO RECUPERADA (CONTEXTO RAG) ===
{contexto}

=== HISTÓRICO DA CONVERSA ===
{historia}

=== PERGUNTA ATUAL DO USUÁRIO ===
{pergunta}
"""
