import pandas as pd
import csv
import io


def detect_delimiter(file):

    """
    Detecta automaticamente o delimitador de um CSV
    """

    sample = file.read(4096).decode("utf-8")

    file.seek(0)

    sniffer = csv.Sniffer()

    dialect = sniffer.sniff(sample)

    return dialect.delimiter


def load_dataset(file):

    """
    Carrega CSV ou Excel automaticamente
    """

    filename = file.name.lower()


    if filename.endswith(".csv"):

        try:

            delimiter = detect_delimiter(file)

            df = pd.read_csv(
                file,
                delimiter=delimiter,
                encoding="utf-8"
            )

        except:

            file.seek(0)

            df = pd.read_csv(
                file,
                delimiter=";",
                encoding="latin1"
            )


    elif filename.endswith(".xlsx") or filename.endswith(".xls"):

        df = pd.read_excel(file)

    else:

        raise ValueError("Formato de arquivo não suportado.")


    # Limpeza basicona


    df.columns = df.columns.str.strip()

    df = df.dropna(how="all")

    df = df.reset_index(drop=True)

    return df