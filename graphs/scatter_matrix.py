import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df["runtime_per_try"] = metrics_df["Runtime"] / metrics_df["Tries"]
metrics_df["Peak memory"] = metrics_df["Peak memory"]
metrics_df["tpkl_change"] = (metrics_df["TPKL Original-Fixed"] - metrics_df["TPKL Original-Generated"])
metrics_df["variation_change"] = (metrics_df["Pattern variation fixed"] - metrics_df["Pattern variation generated"])
metrics_df["difficulty_change"] = (metrics_df["Difficulty fixed"] - metrics_df["Difficulty generated"])
metrics_df["Tries"] = metrics_df["Tries"]

df = metrics_df[["patcher", "tpkl_change", "variation_change", "difficulty_change", "runtime_per_try", "Peak memory"]].copy()

with sns.color_palette("Paired"):
    g = sns.pairplot(df, hue="patcher", markers=["8", "s", "p", "P", "h", "D"])
    g.map_lower(sns.kdeplot, levels=3, color=".2")

    plt.show()