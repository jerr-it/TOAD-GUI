import os
import pandas as pd
import matplotlib.pyplot as plt

from patching.metrics import metrics

METRICS_DF_PATH = "./data/metrics.csv"


def load_metrics_df() -> pd.DataFrame:
    return pd.read_csv(METRICS_DF_PATH)


def total_average(mdf: pd.DataFrame, metric: str, unit: str, generator: str | None = None):
    # Filter out all rows whose 'level' column does not contain generator
    if generator is not None:
        mdf = mdf[mdf["level"].str.contains(generator)]

    # Group by 'patcher' column
    mdf = mdf.groupby("patcher")

    # Calculate the mean of the 'metric' column
    mdf = mdf[metric].median()

    # Sort the values in descending order
    mdf = mdf.sort_values(ascending=False)

    # Plot the values
    mdf.plot.barh()
    plt.xlabel(f"{metric} ({unit})")
    plt.ylabel("Patcher")
    group_name = generator if generator is not None else "All"
    plt.title(f"Average {metric} ({unit}) per Patcher ({group_name})")
    plt.tight_layout()
    # plt.savefig(f"./data/{metric}_per_patcher.png")
    plt.show()
    

    
    

metrics_df = load_metrics_df()

total_average(metrics_df.copy(), "Runtime", "s")
total_average(metrics_df, "Runtime", "s", "1-3")
