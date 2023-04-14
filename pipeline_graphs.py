import os
import pandas as pd
import matplotlib.pyplot as plt

from patching.metrics.metric import metrics


def list_metric_files(metric: str) -> list[str]:
    """
    List all files for a given metric. Every metric has its own file.
    :param metric: Name of the metric
    :return: Paths to all files for the given metric
    """
    base_path: str = os.path.join(os.path.curdir, "data")
    file_names: list[str] = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == metric + ".csv":
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


for metric in metrics:
    file_names: list[str] = list_metric_files(metric["name"])
    data: pd.DataFrame = aggregate_dataframes(file_names)

    # Group data by column 'patcher' and calculate the mean for each group
    grouped_data = data.groupby("patcher")["value"].mean()

    plt.figure(figsize=(10, 5))
    ax = grouped_data.plot(kind="bar")
    ax.set_xticklabels(grouped_data.index, rotation=0)

    plt.xlabel("Patcher")
    plt.ylabel(metric["name"] + " (" + metric["unit"] + ")")

    plt.title("Average " + metric["name"] + " per patcher")

    plt.show()
