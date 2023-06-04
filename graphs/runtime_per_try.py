import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df["runtime_per_try"] = metrics_df["Runtime"] / metrics_df["Tries"]
runtime_per_try_df = metrics_df[["generator", "patcher", "runtime_per_try"]].copy()
runtime_per_try_df = runtime_per_try_df.groupby(["generator", "patcher"]).mean().reset_index()
runtime_per_try_df = runtime_per_try_df.pivot(index="patcher", columns="generator", values="runtime_per_try")

f, ax = plt.subplots(figsize=(20, 5))

ax.set_title("Runtime per try (mean)")
ax.title.set_size(20)

# Make sure the heatmap is square
ax.set_aspect("equal")

sns.heatmap(runtime_per_try_df, annot=True, fmt=".2f", linewidths=.5, ax=ax)

plt.show()