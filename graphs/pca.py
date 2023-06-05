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
metrics_df["tpkl_change"] = (metrics_df["TPKL Original-Fixed"] - metrics_df["TPKL Original-Generated"]).abs()
metrics_df["variation_change"] = (metrics_df["Pattern variation fixed"] - metrics_df["Pattern variation generated"]).abs()
metrics_df["difficulty_change"] = (metrics_df["Difficulty fixed"] - metrics_df["Difficulty generated"]).abs()
metrics_df["Tries"] = metrics_df["Tries"]

df = metrics_df[["patcher", "Runtime", "Peak memory", "tpkl_change", "variation_change", "difficulty_change", "Tries"]].copy()

y = metrics_df[["patcher"]].copy()
X = metrics_df[["Runtime", "Peak memory", "tpkl_change", "variation_change", "difficulty_change", "Tries"]].copy()

x_scaled = StandardScaler().fit_transform(X)

pca = PCA(n_components=2)

pca_features = pca.fit_transform(x_scaled)

pca_df = pd.DataFrame(
    data=pca_features,
    columns=["PC1", "PC2"]
)

pca_df["target"] = y

with sns.color_palette("Paired"):
    g = sns.jointplot(
        data=pca_df,
        x="PC1",
        y="PC2",
        hue="target",
    )

    plt.show()
