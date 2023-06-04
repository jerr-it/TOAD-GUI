import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

jointplot_df = metrics_df[["patcher", "Runtime", "Peak memory"]].copy()
jointplot_df["Peak memory"] = jointplot_df["Peak memory"] / 1000

plot = sns.jointplot(
    data=jointplot_df,
    x="Runtime",
    y="Peak memory",
    hue="patcher",
    height=10,
)
plot.set_axis_labels("Runtime [s]", "Peak memory [kB]")

plt.show()