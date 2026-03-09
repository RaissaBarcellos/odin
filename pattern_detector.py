import pandas as pd
import numpy as np
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def detect_patterns(df, profile=None):

    insights = []

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()


    # Estatísticas


    for col in numeric_cols:

        series = df[col].dropna()

        if len(series) == 0:
            continue

        mean = int(round(series.mean()))
        max_val = int(round(series.max()))
        min_val = int(round(series.min()))

        insights.append(f"A média de {col} é {mean}")
        insights.append(f"O maior valor de {col} é {max_val}")
        insights.append(f"O menor valor de {col} é {min_val}")


    # Outliers (IQR)


    for col in numeric_cols:

        series = df[col].dropna()

        if len(series) < 5:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = series[(series < lower) | (series > upper)]

        if len(outliers) > 0:

            insights.append(
                f"Foram detectados {len(outliers)} valores incomuns na variável {col}"
            )


    # Correlação

    if len(numeric_cols) >= 2:

        corr_matrix = df[numeric_cols].corr()

        for i in range(len(numeric_cols)):
            for j in range(i + 1, len(numeric_cols)):

                col1 = numeric_cols[i]
                col2 = numeric_cols[j]

                # ignorar nomes muito parecidos
                if similar(col1, col2) > 0.8:
                    continue

                # ignorar colunas que são subconjunto do nome
                if col1.lower() in col2.lower() or col2.lower() in col1.lower():
                    continue

                corr = corr_matrix.loc[col1, col2]

                # ignorar correlação quase perfeita (variáveis derivadas)
                if abs(corr) > 0.95:
                    continue

                if abs(corr) > 0.7:

                    insights.append(
                        f"Existe relação entre {col1} e {col2} (coeficiente {round(corr,2)})"
                    )


    # Concentração / desigualdade

    for col in numeric_cols:

        series = df[col].dropna()

        if len(series) < 10:
            continue

        q90 = series.quantile(0.9)
        q50 = series.quantile(0.5)

        if q90 > q50 * 3:

            insights.append(
                f"Os valores de {col} apresentam forte concentração em poucas observações"
            )


    # Categorias dominantes


    for col in categorical_cols:

        counts = df[col].value_counts()

        if len(counts) == 0:
            continue

        top = counts.iloc[0]
        total = counts.sum()

        if top / total > 0.6:

            category = counts.index[0]

            insights.append(
                f"A categoria '{category}' é dominante na variável {col}"
            )


    # Remover insights duplicados


    insights = list(set(insights))

    return insights