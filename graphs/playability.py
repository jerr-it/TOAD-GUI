import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme()
df: pd.DataFrame = pd.read_csv("../data/attempts.csv")

df = df[["generator", "agent", "share"]].copy()

df = df.pivot(index="agent", columns="generator", values="share")

df = df.sort_values(df.first_valid_index(), axis=1)

row_averages = df.mean(axis=1)
col_averages = df.mean(axis=0)

vmin = df.values.min()
vmax = df.values.max()

fig, axs = plt.subplots(2, 2, figsize=(10, 3), gridspec_kw={'width_ratios': [0.92, 0.08], 'height_ratios': [0.7, 0.3]})

sns.heatmap(df, annot=True, cbar=False, ax=axs[0, 0], vmin=vmin, vmax=vmax, square=True)
axs[0, 0].set_title('Share of unplayable levels')
axs[0, 0].set_xlabel("Generator")
axs[0, 0].set_ylabel("Agent")

sns.heatmap(row_averages.to_frame(), annot=True, cbar=True, ax=axs[0, 1], vmin=vmin, vmax=vmax, square=True)
axs[0, 1].set_title('')
axs[0, 1].set_ylabel("Row Averages")

sns.heatmap(col_averages.to_frame().T, annot=True, cbar=False, ax=axs[1, 0], vmin=vmin, vmax=vmax, square=True)
axs[1, 0].set_title('')
axs[1, 0].set_xlabel("Column Averages")

axs[1, 0].set_xticks([])
axs[1, 0].set_yticks([])
axs[0, 1].set_xticks([])
axs[0, 1].set_yticks([])
axs[1, 1].set_xticks([])
axs[1, 1].set_yticks([])
axs[1, 1].axis("off")

plt.tight_layout()

plt.show()