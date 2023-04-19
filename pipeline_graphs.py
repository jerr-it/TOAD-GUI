import os
import pandas as pd
import matplotlib.pyplot as plt

from patching.metrics import metrics


def list_metric_files() -> list[str]:
    """
    List all metric files in the data directory.
    :return: Paths to all files containing metric data
    """
    base_path: str = os.path.join(os.path.curdir, "data")
    file_names: list[str] = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "metrics.csv":
                file_names.append(os.path.join(root, file))

    return file_names


def aggregate_dataframes(file_names: list[str]) -> pd.DataFrame:
    """
    Aggregate all dataframes from the given files into one dataframe.
    CSV files are split, there is one per generator.
    :param file_names: File names to the CSV files
    :return: Aggregated dataframe
    """
    dataframes = []

    for file_name in file_names:
        dataframes.append(pd.read_csv(file_name))

    return pd.concat(dataframes)


file_names: list[str] = list_metric_files()
data: pd.DataFrame = aggregate_dataframes(file_names)

for metric in metrics:
    # Group data by column 'patcher' and calculate the mean for each group
    grouped_data = data.groupby("patcher")[metric["name"]].mean()

    plt.figure(figsize=(10, 5))
    ax = grouped_data.plot(kind="bar")
    ax.set_xticklabels(grouped_data.index, rotation=0)

    plt.xlabel("Patcher")
    plt.ylabel(metric["name"] + " (" + metric["unit"] + ")")

    plt.title("Average " + metric["name"])

    plt.show()
