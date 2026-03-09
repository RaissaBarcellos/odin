import streamlit as st
import pandas as pd
import time
import requests

from data_loader import load_dataset
from variable_profiler import profile_variables, get_categorical_columns, get_numeric_columns
from pattern_detector import detect_patterns
from visualizer import generate_visualizations
from visual_explainer import explain_visualization
from data_integration import clean_merged_columns, suggest_integration_key
from visual_pattern_analyzer import analyze_visual_pattern
from visual_llm_explainer import explain_visual_with_llm



# Configuração da página


st.set_page_config(
    page_title="ODIN — OpenData Interpreter",
    layout="wide"
)

st.title("ODIN — OpenData Interpreter")

st.sidebar.image("odin.png", width=200)

st.markdown(
"""
Protótipo para **interpretação automática de datasets tabulares**.
"""
)

st.divider()



# Integração de datasets


def integrate_datasets(dfs, key):

    df = dfs[0]

    for other in dfs[1:]:

        if key and key in df.columns and key in other.columns:

            df = df.merge(other, on=key, how="outer")

        else:

            df = pd.concat([df, other], axis=0)

    return df



# Interpretação geral com LLM


def generate_global_interpretation(insights):

    if not insights:
        return "Nenhum padrão relevante foi encontrado nos dados."

    insights_text = "\n".join(insights[:6])

    prompt = f"""
CONTEXTO
Você é um assistente que ajuda cidadãos a entender dados públicos.

DADOS
Os seguintes resultados foram detectados automaticamente:

{insights_text}

REGRAS
- Use apenas as informações fornecidas
- Não invente números
- Use linguagem simples
- Evite termos técnicos
- Escreva no máximo 4 frases curtas

TAREFA
Explique os principais padrões encontrados nesses dados.

RESPOSTA
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=500
        )

        text = response.json()["response"]

        if "RESPOSTA" in text:
            text = text.split("RESPOSTA")[-1]

        return text.strip()

    except Exception as e:

        return f"⚠️ Não foi possível conectar ao Ollama: {e}"



st.sidebar.header("Configuração")

files = st.sidebar.file_uploader(
    "Carregar datasets",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)



if files:

    start_time = time.time()

    dfs = []

    # carregar datasets
    for file in files:

        df = load_dataset(file)
        dfs.append(df)

    # detectar todas as colunas possíveis
    all_columns = list(set().union(*[d.columns for d in dfs]))

    # sugerir automaticamente chave de integração
    suggested_key = suggest_integration_key(dfs)

    if suggested_key:
        st.sidebar.info(
            f"Sugestão automática: usar a coluna '{suggested_key}' para integrar os datasets."
        )

    # seletor para o usuário
    integration_key = st.sidebar.selectbox(
        "Coluna para integrar datasets",
        ["Nenhuma"] + all_columns,
        index=(all_columns.index(suggested_key) + 1) if suggested_key else 0
    )

    if integration_key == "Nenhuma":
        integration_key = None

    # integrar datasets
    df = integrate_datasets(dfs, integration_key)

    # limpar colunas duplicadas
    df = clean_merged_columns(df)

    # profiling
    profile = profile_variables(df)

    print("PROFILE ------ ",profile)

    print("NUMERIC:", get_numeric_columns(profile))
    print("CATEGORICAL:", get_categorical_columns(profile))

    # detectar padrões
    insights = detect_patterns(df, profile)

    end_analysis = time.time()

 
    # Métricas


    colA, colB, colC = st.columns(3)

    colA.metric("Registros", len(df))
    colB.metric("Variáveis", len(df.columns))
    colC.metric("Insights detectados", len(insights))

    st.divider()


    # preview


    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.divider()


    # Insights


    st.subheader("Principais padrões encontrados")

    cols = st.columns(3)

    for i, insight in enumerate(insights):
        cols[i % 3].info(insight)

    st.divider()


    # Visualizações


    st.subheader("Visualizações")

    figs = generate_visualizations(df, profile)

    cols = st.columns(2)

    for i, fig_info in enumerate(figs):

        fig = fig_info["figure"]
        x = fig_info.get("x")
        y = fig_info.get("y")
        chart_type = fig_info.get("type")

        with cols[i % 2]:

            st.plotly_chart(fig, use_container_width=True)

            explanation = explain_visualization(
                df,
                chart_type=chart_type,
                x=x,
                y=y
            )

            st.caption(explanation)

    st.divider()


    # Interpretação geral


    st.subheader("Interpretação geral dos dados")

    with st.spinner("Gerando interpretação..."):

        summary = generate_global_interpretation(insights)

    st.info(summary)

    end_llm = time.time()

    st.divider()


    # Desempenho

    st.subheader("Desempenho")

    colX, colY = st.columns(2)

    colX.metric(
        "Tempo de análise",
        f"{end_analysis - start_time:.2f}s"
    )

    colY.metric(
        "Tempo de interpretação",
        f"{end_llm - end_analysis:.2f}s"
    )