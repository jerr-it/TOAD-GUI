import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df["runtime_per_try"] = metrics_df["Runtime"] / metrics_df["Tries"]
metrics_df["Runtime per try [s]"] = metrics_df["runtime_per_try"]
metrics_df["Peak memory [kB]"] = metrics_df["Peak memory"] / 1000

jointplot_df = metrics_df[["patcher", "Runtime per try [s]", "Peak memory [kB]"]].copy()

with sns.color_palette("Paired"):
    ax = sns.pairplot(jointplot_df, hue="patcher", markers=["8", "s", "p", "P", "h", "D"])
    sns.move_legend(ax, "upper right", bbox_to_anchor=(.75, .65))

plt.show()