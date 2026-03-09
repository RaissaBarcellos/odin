from collections import Counter


def clean_merged_columns(df):

    cols = df.columns

    for col in cols:

        if col.endswith("_x"):

            base = col[:-2]

            col_y = base + "_y"

            if col_y in df.columns:

                # combinar valores
                df[base] = df[col].combine_first(df[col_y])

                # remover colunas técnicas
                df = df.drop(columns=[col, col_y])

    return df




def suggest_integration_key(dfs):

    # juntar todos os nomes de colunas
    all_cols = []

    for df in dfs:
        all_cols.extend(df.columns)

    # contar frequência
    counts = Counter(all_cols)

    # colunas que aparecem em mais de um dataset
    candidates = [col for col, count in counts.items() if count > 1]

    if not candidates:
        return None

    # escolher a mais frequente
    best = max(candidates, key=lambda col: counts[col])

    return best