def clean_insights(insights):

    cleaned = []

    for insight in insights:

        text = insight

        # reduzir casas decimais
        import re
        text = re.sub(r"\d+\.\d{3,}", lambda m: f"{float(m.group()):.2f}", text)

        # remover underscores
        text = text.replace("_", " ")

        # remover espaços duplicados
        text = " ".join(text.split())

        cleaned.append(text)

    return cleaned