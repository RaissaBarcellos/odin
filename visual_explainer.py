import numpy as np


def explain_visualization(df, chart_type=None, x=None, y=None):


    # Histograma


    if chart_type == "histogram" and y:

        series = df[y].dropna()

        if len(series) == 0:
            return "Não há dados suficientes para interpretar este gráfico."

        mean = series.mean()
        median = series.median()

        return (
            f"A maior parte dos valores de {y} está concentrada em torno de {int(round(median))}. "
            f"A média observada é aproximadamente {int(round(mean))}"
        )

    # Scatter


    if chart_type == "scatter" and x and y:

        try:

            corr = df[x].corr(df[y])

            if abs(corr) > 0.7:
                relation = "forte"

            elif abs(corr) > 0.4:
                relation = "moderada"

            elif abs(corr) > 0.2:
                relation = "fraca"

            else:
                relation = None

            if relation:

                return (
                    f"Os dados sugerem uma relação {relation} entre {x} e {y}. "
                    f"Quando os valores de {x} aumentam, os valores de {y} tendem a variar na mesma direção."
                )

            else:

                return (
                    f"Não foi observada uma relação clara entre {x} e {y} neste conjunto de dados."
                )

        except:

            return "Não foi possível identificar padrões claros neste gráfico."


    # Boxplot


    if chart_type == "box" and y:

        series = df[y].dropna()

        median = series.median()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        return (
            f"O valor típico de {y} está próximo de {int(round(median))}. "
            f"A maioria dos valores está entre {int(round(q1))} e {int(round(q3))}."
        )


    # Bar chart


    if chart_type == "bar" and x:

        counts = df[x].value_counts()

        if len(counts) == 0:
            return "Não há dados suficientes para interpretar este gráfico."

        top = df.loc[df[x].idxmax()]
        bottom = df.loc[df[x].idxmin()]

        return (
            f"{top[y]} apresenta o maior valor de {x} "
            f"({int(top[x])}), enquanto {bottom[y]} possui o menor "
            f"({int(bottom[x])})."
        )

    return "Este gráfico mostra um padrão presente nos dados."