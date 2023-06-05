import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_generator_column

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df = add_generator_column(metrics_df)
metrics_df["variation_change"] = (metrics_df["Pattern variation fixed"] - metrics_df["Pattern variation generated"]).abs() * 100
df = metrics_df[["generator", "patcher", "variation_change"]].copy()

df = df.groupby(["generator", "patcher"]).mean().reset_index()
df = df.pivot(index="patcher", columns="generator", values="variation_change")

f, ax = plt.subplots(figsize=(20, 5))

ax.set_title("Change in Pattern variation (mean)")
ax.title.set_size(20)

# Make sure the heatmap is square
ax.set_aspect("equal")

plot = sns.heatmap(df, annot=True, fmt=".2f", linewidths=.5, ax=ax)
plot.set_xlabel("Generator")
plot.set_ylabel("Patcher")

plt.show()