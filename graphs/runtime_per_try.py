import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_generator_column

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df = add_generator_column(metrics_df)
metrics_df["runtime_per_try"] = metrics_df["Runtime"] / metrics_df["Tries"]
runtime_per_try_df = metrics_df[["generator", "patcher", "runtime_per_try"]].copy()
runtime_per_try_df = runtime_per_try_df.groupby(["generator", "patcher"]).mean().reset_index()
runtime_per_try_df = runtime_per_try_df.pivot(index="patcher", columns="generator", values="runtime_per_try")

row_averages = runtime_per_try_df.mean(axis=1)
col_averages = runtime_per_try_df.mean(axis=0)

vmin = runtime_per_try_df.values.min()
vmax = runtime_per_try_df.values.max()

fig, axs = plt.subplots(2, 2, figsize=(10, 8), gridspec_kw={'width_ratios': [1, 0.2], 'height_ratios': [1, 0.2]})

sns.heatmap(runtime_per_try_df, annot=True, cbar=False, ax=axs[0, 0], vmin=vmin, vmax=vmax)
axs[0, 0].set_title('Runtime per try (mean) (s)')

sns.heatmap(row_averages.to_frame(), annot=True, cbar=True, ax=axs[0, 1], vmin=vmin, vmax=vmax)
axs[0, 1].set_title('Row Averages')
axs[0, 1].set_ylabel("")

sns.heatmap(col_averages.to_frame().T, annot=True, cbar=False, ax=axs[1, 0], vmin=vmin, vmax=vmax)
axs[1, 0].set_title('')
axs[1, 0].set_xlabel("Column Averages")

overall_average = runtime_per_try_df.values.mean()
sns.heatmap([[overall_average]], annot=True, cbar=False, ax=axs[1, 1], vmin=vmin, vmax=vmax)
axs[1, 1].set_title('Overall Average')

axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])
axs[0, 1].set_xticks([])
axs[0, 1].set_yticks([])
axs[1, 1].set_xticks([])
axs[1, 1].set_yticks([])

plt.tight_layout()

plt.show()