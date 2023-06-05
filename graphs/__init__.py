import pandas as pd

METRICS_DF_PATH = "../data/metrics.csv"

PATCHER_NAMES = ["Wave Function Collapse", "Evolutionary Patterns", "Stitching", "Best fit stitching", "Online"]

GENERATOR_NAMES = [
    "1-1", "1-2", "1-3", "2-1",
    "3-1", "3-3", "4-1", "4-2",
    "5-1", "5-3", "6-1", "6-2",
    "6-3", "7-1", "8-1"
]


def load_metrics_df() -> pd.DataFrame:
    return pd.read_csv(METRICS_DF_PATH)


def add_generator_column(df: pd.DataFrame) -> pd.DataFrame:
    df["generator"] = df["level"].str.extract(r"(\d{1}-\d{1})")
    return df


def add_level_type_column(df: pd.DataFrame) -> pd.DataFrame:
    df["level_type"] = df["generator"].str[-1]
    return df


def add_cumul_difficulty_column(df: pd.DataFrame) -> pd.DataFrame:
    df["cumul_difficulty_orig"] = df["Original rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    df["cumul_difficulty_generated"] = df["Generated rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    df["cumul_difficulty_fixed"] = df["Fixed rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    return df
