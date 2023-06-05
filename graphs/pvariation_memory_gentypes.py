import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_level_type_column, add_generator_column

with sns.color_palette("Paired"):
    metrics_df: pd.DataFrame = load_metrics_df()
    metrics_df["Peak memory"] = metrics_df["Peak memory"] / 1000

    linreg_df = add_generator_column(metrics_df)
    linreg_df = add_level_type_column(linreg_df)
    level_type_df = linreg_df[["patcher", "level_type", "Pattern variation generated", "Peak memory"]].copy()
    level_type_df = level_type_df[level_type_df["patcher"] == "Wave Function Collapse"]

    plot = sns.jointplot(
        data=level_type_df,
        x="Pattern variation generated",
        y="Peak memory",
        hue="level_type",
        kind="kde",
    )
    plot.set_axis_labels("Pattern variation []", "Peak memory [kB]")

    plt.suptitle("WFC peak memory", x=0.8, y=0.95)

    plt.show()
