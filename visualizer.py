import plotly.express as px
import numpy as np

from variable_profiler import (
    get_numeric_columns,
    get_categorical_columns,
    profile_variables
)


def is_informative(series):

    unique_ratio = series.nunique() / len(series)

    if unique_ratio < 0.02:
        return False

    if unique_ratio > 0.95:
        return False

    return True


def generate_visualizations(df, profile):

    figures = []

    numeric_cols = get_numeric_columns(profile)
    categorical_cols = get_categorical_columns(profile)

    # Ranking


    if numeric_cols and categorical_cols:

        num_col = numeric_cols[0]
        cat_col = categorical_cols[0]

        df_sorted = df.sort_values(num_col, ascending=False).head(10)

        fig = px.bar(
            df_sorted,
            x=num_col,
            y=cat_col,
            orientation="h",
            title=f"Top 10 valores de {num_col} por {cat_col}"
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        figures.append({
            "figure": fig,
            "x": num_col,
            "y": cat_col,
            "type": "bar"
        })


    # Scatter

    if len(numeric_cols) >= 2:

        for i in range(len(numeric_cols)):

            for j in range(i + 1, len(numeric_cols)):

                x = numeric_cols[i]
                y = numeric_cols[j]

                try:

                    corr = df[x].corr(df[y])

                    if abs(corr) > 0.2:

                        fig = px.scatter(
                            df,
                            x=x,
                            y=y,
                            title=f"Relação entre {x} e {y} — cada ponto representa um registro"
                        )

                        figures.append({
                            "figure": fig,
                            "x": x,
                            "y": y,
                            "type": "scatter"
                        })

                        break

                except:
                    pass

            if len(figures) > 1:
                break

    # Boxplot

    if len(numeric_cols) >= 1:

        col = numeric_cols[0]

        fig = px.box(
            df,
            y=col,
            title=f"Distribuição e possíveis valores extremos de {col} — ajuda a identificar valores muito diferentes do restante"
        )

        figures.append({
            "figure": fig,
            "x": None,
            "y": col,
            "type": "box"
        })

    # ---------------------------
    # Gráfico categórico
    # ---------------------------

    # if len(categorical_cols) >= 1:

    #     cat = categorical_cols[0]

    #     counts = df[cat].value_counts().reset_index()

    #     counts.columns = [cat, "count"]

    #     fig = px.bar(
    #         counts,
    #         x=cat,
    #         y="count",
    #         title=f"Distribuição das categorias de {cat} — mostra quantos registros existem em cada categoria"
    #     )

    #     figures.append({
    #         "figure": fig,
    #         "x": cat,
    #         "y": "count",
    #         "type": "bar"
    #     })

    return figures