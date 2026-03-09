import pandas as pd


def analyze_visual_pattern(df, chart_type, x=None, y=None):

    insights = []

    if chart_type == "histogram" and x:

        mean = int(df[x].mean())
        median = int(df[x].median())

        insights.append(
            f"O valor médio de {x} é {mean}"
        )

        insights.append(
            f"A mediana de {x} é {median}"
        )

    elif chart_type == "scatter" and x and y:

        corr = df[x].corr(df[y])

        insights.append(
            f"A correlação entre {x} e {y} é {round(corr,2)}"
        )

    elif chart_type == "bar" and x:

        counts = df[x].value_counts()

        top = counts.index[0]

        insights.append(
            f"A categoria mais frequente em {x} é {top}"
        )

    return insights