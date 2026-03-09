import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def explain_visual_with_llm(patterns):

    patterns_text = "\n".join(patterns)

    prompt = f"""
CONTEXTO
Você está ajudando cidadãos a entender gráficos de dados públicos.

DADOS OBSERVADOS
{patterns_text}

TAREFA
Explique o que o gráfico mostra.

REGRAS
- Use linguagem simples
- Evite termos técnicos
- Explique o que os dados indicam
- Use no máximo 3 frases

EXPLICAÇÃO
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 80
            }
        }
    )

    return response.json()["response"]