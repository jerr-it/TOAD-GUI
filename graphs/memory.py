import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

runtime_per_try_df = metrics_df[["generator", "patcher", "Peak memory"]].copy()
runtime_per_try_df["Peak memory"] = runtime_per_try_df["Peak memory"] / 1000
runtime_per_try_df = runtime_per_try_df.groupby(["generator", "patcher"]).mean().reset_index()
runtime_per_try_df = runtime_per_try_df.pivot(index="patcher", columns="generator", values="Peak memory")

f, ax = plt.subplots(figsize=(20, 5))

ax.set_title("Peak memory (kB) (mean)")
ax.title.set_size(20)

# Make sure the heatmap is square
ax.set_aspect("equal")

plot = sns.heatmap(runtime_per_try_df, annot=True, fmt=".2f", linewidths=.5, ax=ax)
plot.set_xlabel("Generator")
plot.set_ylabel("Patcher")

plt.show()