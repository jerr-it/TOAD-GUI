import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

linreg_df = metrics_df[["patcher", "Pattern variation generated", "Peak memory"]].copy()
linreg_df["Peak memory"] = linreg_df["Peak memory"] / 1000

plot = sns.lmplot(
    data=linreg_df,
    x="Pattern variation generated",
    y="Peak memory",
    hue="patcher",
)
plot.set_axis_labels("Pattern variation []", "Peak memory [kB]")

plt.show()