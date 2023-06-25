import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from graphs import load_metrics_df

sns.set_theme()
metrics_df: pd.DataFrame = load_metrics_df()

metrics_df["Runtime"] = metrics_df["Runtime"]
metrics_df["Peak memory"] = metrics_df["Peak memory"]
metrics_df["tpkl_change"] = (metrics_df["TPKL Original-Fixed"] - metrics_df["TPKL Original-Generated"])
metrics_df["variation_change"] = (metrics_df["Pattern variation fixed"] - metrics_df["Pattern variation generated"])
metrics_df["difficulty_change"] = (metrics_df["Difficulty fixed"] - metrics_df["Difficulty generated"])
metrics_df["Tries"] = metrics_df["Tries"]

y = metrics_df[["patcher"]].copy()
X = metrics_df[["tpkl_change", "variation_change", "difficulty_change", "Runtime", "Peak memory", "Tries"]].copy()

x_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)

pca_features = pca.fit_transform(x_scaled)

print(pca.explained_variance_ratio_)
pca_df = pd.DataFrame(
    data=pca_features,
    columns=["PC1", "PC2"]
)

pca_df["target"] = y

fig, axes = plt.subplots(2, 5, figsize=(30, 10), subplot_kw={'aspect': 'equal'})
fig.suptitle("PCA [Runtime, Memory, Tries, TPKL change, variation change, difficulty change]")

colors = sns.color_palette("Paired")
for idx, patcher in enumerate(["Wave Function Collapse", "Evolutionary Patterns", "Stitching", "Best fit stitching", "Online"]):
    with sns.color_palette("Paired"):
        g = sns.scatterplot(
            data=pca_df.loc[pca_df["target"] == patcher],
            x="PC1",
            y="PC2",
            ax=axes.flatten()[idx],
            color=colors[idx]
        )
        axes.flatten()[idx].set_title(patcher)

for idx, patcher in enumerate(["Wave Function Collapse", "Evolutionary Patterns", "Stitching", "Best fit stitching", "Online"]):
    with sns.color_palette("Paired"):
        g = sns.kdeplot(
            data=pca_df.loc[pca_df["target"] == patcher],
            x="PC1",
            y="PC2",
            ax=axes.flatten()[idx+5],
            color=colors[idx]
        )

for ax in axes.flatten():
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

plt.tight_layout()
plt.show()