import os
import json

def carregar_arquivos_base_conhecimento(data_dir: str = "data") -> str:
    """Varre recursivamente a pasta data/ e concatena todo o conhecimento disponível."""
    conteudos = []
    
    for root, _, files in os.walk(data_dir):
        for file in files:
            path = os.path.join(root, file)
            try:
                if file.endswith((".md", ".txt")):
                    with open(path, "r", encoding="utf-8") as f:
                        conteudos.append(f"--- DOCUMENTO: {file} ---\n" + f.read())
                elif file.endswith(".json"):
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        conteudos.append(f"--- DOCUMENTO JSON: {file} ---\n" + json.dumps(data, ensure_ascii=False, indent=2))
            except Exception as e:
                print(f"Erro ao ler arquivo {path}: {e}")
                
    return "\n\n".join(conteudos)

def buscar_contexto_relevante(query: str, data_dir: str = "data") -> str:
    """Busca o contexto em data/ para a pergunta fornecida (RAG Leve / Híbrido)."""
    base_conhecimento = carregar_arquivos_base_conhecimento(data_dir)
    return base_conhecimento
