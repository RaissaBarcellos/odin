import pandas as pd


def detect_variable_type(series):

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    if pd.api.types.is_string_dtype(series):
        return "categorical"

    return "categorical"


def profile_variables(df):

    profile = {}

    for col in df.columns:

        series = df[col]

        var_type = detect_variable_type(series)

        unique_count = series.nunique()
        total = len(series)

        unique_ratio = unique_count / total if total > 0 else 0

        info = {
            "type": var_type,
            "missing": int(series.isna().sum()),
            "unique": int(unique_count),
            "unique_ratio": float(unique_ratio)
        }

        # detectar possível ID
        if unique_ratio > 0.95 and var_type == "numeric" and "id" in col.lower():
            info["possible_id"] = True
        else:
            info["possible_id"] = False

        if var_type == "numeric":

            info.update({
                "mean": float(series.mean()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max())
            })

        profile[col] = info

    return profile


def get_numeric_columns(profile):

    return [
        col for col, meta in profile.items()
        if meta["type"] == "numeric"
        and not meta["possible_id"]
    ]


def get_categorical_columns(profile):

    return [
        col for col, meta in profile.items()
        if meta["type"] == "categorical"
        and not meta["possible_id"]
        and meta["unique"] <= 200
    ]


def get_datetime_columns(profile):

    return [
        col for col, meta in profile.items()
        if meta["type"] == "datetime"
    ]