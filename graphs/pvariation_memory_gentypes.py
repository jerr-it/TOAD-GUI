import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_level_type_column, add_generator_column

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

linreg_df = add_generator_column(metrics_df)
linreg_df = add_level_type_column(linreg_df)
linreg_df = linreg_df[["patcher", "level_type", "Pattern variation generated", "Peak memory"]].copy()
linreg_df = linreg_df[linreg_df["patcher"] == "Wave Function Collapse"]
linreg_df["Peak memory"] = linreg_df["Peak memory"] / 1000

plot = sns.lmplot(
    data=linreg_df,
    x="Pattern variation generated",
    y="Peak memory",
    hue="level_type",
    fit_reg=False
)
plot.set_axis_labels("Pattern variation []", "Peak memory [kB]")

plt.show()