import pandas as pd

METRICS_DF_PATH = "../data/metrics.csv"

PATCHER_NAMES = ["Online", "Stitching", "Best fit stitching", "Evolutionary Patterns", "Wave Function Collapse"]

GENERATOR_NAMES = [
    "1-1", "1-2", "1-3", "2-1",
    "3-1", "3-3", "4-1", "4-2",
    "5-1", "5-3", "6-1", "6-2",
    "6-3", "7-1", "8-1"
]


LEVEL_TYPES = {
    "1-1": "Overworld",
    "1-2": "Cave",
    "1-3": "Platforms",
    "2-1": "Overworld",
    "3-1": "Overworld",
    "3-3": "Platforms",
    "4-1": "Overworld",
    "4-2": "Cave",
    "5-1": "Overworld",
    "5-3": "Platforms",
    "6-1": "Overworld",
    "6-2": "Overworld",
    "6-3": "Platforms",
    "7-1": "Overworld",
    "8-1": "Overworld",
}


def load_metrics_df() -> pd.DataFrame:
    return pd.read_csv(METRICS_DF_PATH)


def add_generator_column(df: pd.DataFrame) -> pd.DataFrame:
    df["generator"] = df["level"].str.extract(r"(\d{1}-\d{1})")
    return df


def add_level_type_column(df: pd.DataFrame) -> pd.DataFrame:
    df["level_type"] = df["generator"].apply(lambda x: LEVEL_TYPES[x])
    return df


def add_cumul_difficulty_column(df: pd.DataFrame) -> pd.DataFrame:
    df["cumul_difficulty_orig"] = df["Original rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    df["cumul_difficulty_generated"] = df["Generated rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    df["cumul_difficulty_fixed"] = df["Fixed rolling difficulty"].str.split("|").apply(lambda x: sum([float(i) for i in x]))
    return df
