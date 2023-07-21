import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from graphs import load_metrics_df, add_generator_column

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df = add_generator_column(metrics_df)
df = metrics_df[["generator", "patcher", "Tries"]].copy()

df = df.groupby(["generator", "patcher"]).mean().reset_index()
df = df.pivot(index="patcher", columns="generator", values="Tries")

row_averages = df.mean(axis=1)
col_averages = df.mean(axis=0)

vmin = df.values.min()
vmax = df.values.max()

w = 0.857
fig, axs = plt.subplots(2, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [0.92, 0.08], 'height_ratios': [w, 1 - w]})

sns.heatmap(df, annot=True, cbar=False, ax=axs[0, 0], vmin=vmin, vmax=vmax, square=True)
axs[0, 0].set_title('Tries (mean)')
axs[0, 0].set_xlabel("Generator")
axs[0, 0].set_ylabel("Patcher")

sns.heatmap(row_averages.to_frame(), annot=True, cbar=True, ax=axs[0, 1], vmin=vmin, vmax=vmax, square=True)
axs[0, 1].set_title('Row Averages')
axs[0, 1].set_ylabel("")

sns.heatmap(col_averages.to_frame().T, annot=True, cbar=False, ax=axs[1, 0], vmin=vmin, vmax=vmax, square=True)
axs[1, 0].set_title('')
axs[1, 0].set_xlabel("Column Averages")

overall_average = df.values.mean()
sns.heatmap([[overall_average]], annot=True, cbar=False, ax=axs[1, 1], vmin=vmin, vmax=vmax, square=True)
axs[1, 1].set_title('Overall Average')

axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])
axs[0, 1].set_xticks([])
axs[0, 1].set_yticks([])
axs[1, 1].set_xticks([])
axs[1, 1].set_yticks([])

plt.tight_layout()

plt.show()