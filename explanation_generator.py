import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def select_main_insights(insights, max_items=6):

    if not insights:
        return []

    priority_keywords = [
        "relação",
        "correlação",
        "concentração",
        "dominante",
        "incomuns",
        "maior valor",
        "menor valor"
    ]

    selected = []

    for insight in insights:

        text = insight.lower()

        if any(word in text for word in priority_keywords):
            selected.append(insight)

    if not selected:
        selected = insights

    unique = list(dict.fromkeys(selected))

    return unique[:max_items]


def generate_explanation(insights):

    if not insights:
        return "Nenhum padrão relevante foi encontrado neste conjunto de dados."

    main_insights = select_main_insights(insights)

    insights_text = "\n".join(main_insights)

    prompt = f"""
CONTEXTO
Você é um assistente que ajuda cidadãos a entender dados públicos.

DADOS
Os seguintes resultados foram detectados automaticamente:

{insights_text}

REGRAS
- Use apenas as informações fornecidas
- Não invente números
- Explique em português simples
- Evite linguagem técnica

TAREFA
Explique os principais padrões encontrados nesses dados.

FORMATO
Um parágrafo bem explicativo.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    text = response.json()["response"]

    return text.strip()