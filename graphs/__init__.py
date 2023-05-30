import pandas as pd

METRICS_DF_PATH = "../data/metrics.csv"

PATCHER_NAMES = ["Wave Function Collapse", "Evolutionary Patterns", "Stitching", "Best fit stitching"]

GENERATOR_NAMES = [
    "1-1", "1-2", "1-3", "2-1",
    "3-1", "3-3", "4-1", "4-2",
    "5-1", "5-3", "6-1", "6-2",
    "6-3", "7-1", "8-1"
]


def load_metrics_df() -> pd.DataFrame:
    return pd.read_csv(METRICS_DF_PATH)
