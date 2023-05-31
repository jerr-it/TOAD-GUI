import concurrent.futures
import os
import sys
import time
import traceback

import numpy as np
import pandas as pd
import py4j.java_gateway

from patching import patchers
from patching.metrics import metrics
from utils.level_utils import place_a_mario_token
from utils.mario_ai import MarioAI, AgentType
from utils.token_defs import MARIO_PATH_TOKEN

REPAIR_STAGE_THREADS = 12


def list_generators() -> list[str]:
    """
    List all generators for which there are levels generated by the previous pipeline stage.
    :return: List of paths to all generators
    """
    files: list[str] = []

    basepath: str = os.path.join(os.path.curdir, "data")
    if not os.path.exists(basepath):
        os.mkdir(basepath)

    with os.scandir(basepath) as it:
        for entry in it:
            if entry.is_dir():
                files.append(str(entry.name))

    return files


def list_levels(generator_path: str) -> list[str]:
    """
    Lists all levels inside the given generators data directory
    :param generator_path: path to level files for a given generator
    :return: list of levels to be tested inside that directory (path
    """
    level_files: list[str] = []

    with os.scandir(generator_path) as it:
        for entry in it:
            if entry.name.startswith("level"):
                path = os.path.join(generator_path, str(entry.name))
                level_files.append(path)

    return level_files


def parse_broken_level(level_path: str) -> (list[str], float):
    """
    Parses a file containing a broken level
    Always contains the mario agents progress in the first line.
    All other following lines are rows of the level
    :param level_path:
    :return:
    """
    level: list[str]
    progress: float

    with open(level_path, "r") as f:
        lines = f.readlines()
        progress = float(lines.pop(0))
        level = [line.rstrip() for line in lines]

    return level, progress


def already_done(level_path: str, patcher: str, metrics_df: pd.DataFrame) -> bool:
    """
    Returns true if we already ran the given patcher on the given level
    :param level_path: path to the level
    :param patcher: patcher to apply
    :param metrics_df: df containing already completed runs
    :return: True if the patcher was already run on that level
    """
    if metrics_df.empty:
        return False

    return ((metrics_df["level"] == level_path) & (metrics_df["patcher"] == patcher)).any()


def load_original_level(generator_path: str) -> list[str]:
    """
    Loads the original level the given generator was trained on
    :param generator_path: Path to the generator
    :return: Original level the generator was trained on
    """
    level_id: str = generator_path.split("_")[2]
    level_path: str = os.path.join(os.path.curdir, "levels", "originals", f"lvl_{level_id}.txt")

    level: list[str]
    with open(level_path, "r") as f:
        level = [line.rstrip() for line in f.readlines()]

    return level


def calculate_broken_range(
        progress: float,
        level_width: int,
        level_height: int,
        range_width: int = 5
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Calculates a range thats to be replaced by the patcher
    :param progress: Progress the mario agent made in %
    :param level_width: Total width of the level (blocks)
    :param level_height: Total height of the level (blocks)
    :param range_width: How wide the range is supposed to be in each direction
    :return: Range
    """
    block_progress = int(float(level_width) * progress)

    return (
        (max(block_progress - range_width, 0), min(block_progress + range_width, level_width - 2)),
        (0, level_height)
    )


def check_mario_token(level: list[str]) -> list[str]:
    m_exists = False
    for line in level:
        if 'M' in line:
            m_exists = True
            break
    if not m_exists:
        return place_a_mario_token(level)
    return level


def mark_path(level: list[str], result: py4j.java_gateway.JavaObject) -> list[str]:
    nplevel = np.array([list(row) for row in level])
    height = len(level)
    width = len(level[0])

    path = result.getMarioPath()
    for position in path:
        x = int(position.getX() * 16.0)
        y = int(position.getY() * 16.0)

        if x < 0 or x >= width:
            continue

        if y >= height:
            continue

        nplevel[y][x] = MARIO_PATH_TOKEN

    return ["".join(row) for row in nplevel]


def repair_level(
        level_path: str,
        generator_path: str,
        metrics_df: pd.DataFrame
) -> (str, pd.DataFrame, dict[str, list[str]]):
    """
    Repairs a given broken level using all available repair mechanisms and
    evaluates their performance with the given metrics
    :param level_path: Path to the level thats to be repaired
    :param generator_path: Path to the generator the level was created from
    :param metrics_df: Existing metrics data, to avoid repairing a level twice
    :return: (
        level path
        Dataframe containing metrics evaluated on the different patchers,
        dict of levels fixed (one per patcher)
    )
    """
    try:
        generated_level, progress = parse_broken_level(level_path)
        level_width: int = len(generated_level[0])
        level_height: int = len(generated_level)

        original_level = load_original_level(generator_path)
        with MarioAI() as mario:
            metrics_data = []
            level_dict = {}

            for patcher_name, patcher in patchers.items():
                if already_done(level_path, patcher_name, metrics_df):
                    print(f"Skipping {patcher_name} for {level_path}")
                    continue

                print(f"Applying {patcher_name} to {level_path}")
                metrics_data.insert(0, {"level": level_path, "patcher": patcher_name})

                original_result = mario.evaluate_level(original_level.copy(), AgentType.AstarDynamicPlanning, False, 4000, 30)
                generated_result = mario.evaluate_level(generated_level.copy(), AgentType.AstarDynamicPlanning, False, 4000, 30)

                for metric in metrics:
                    metric.pre_hook(
                        original_level.copy(),
                        original_result,
                        generated_level.copy(),
                        generated_result
                    )

                fixed_level: list[str] = generated_level.copy()
                current_progress = progress
                mario_result = generated_result

                while current_progress < 0.99:
                    broken_range = calculate_broken_range(current_progress, level_width, level_height)

                    try:
                        fixed_level = check_mario_token(
                            patcher.patch(original_level, fixed_level, broken_range, generator_path, mario_result)
                        )

                        mario_result = mario.evaluate_level(fixed_level, AgentType.AstarDynamicPlanning, False, 4000, 30)
                        current_progress = mario_result.getCompletionPercentage()
                    except Exception as e:
                        print(f"Patcher {patcher_name} on level {level_path} threw exception: {e}", file=sys.stderr)

                    for metric in metrics:
                        metric.iter_hook(mario_result, fixed_level)

                for metric in reversed(metrics):
                    result = metric.post_hook(
                        mario_result,
                        original_level,
                        generated_level,
                        fixed_level
                    )

                    for metric_name, metric_value in result.items():
                        metrics_data[0][metric_name] = metric_value

                fixed_level = mark_path(fixed_level, mario_result)
                level_dict[patcher_name] = fixed_level
    except Exception as e:
        print(f"Fixing process ended unexpectedly: {traceback.format_exc()}", file=sys.stderr)

    return level_path, pd.DataFrame(metrics_data), level_dict


def read_or_create_metrics_csv() -> pd.DataFrame:
    metrics_path: str = os.path.join(os.path.curdir, "data", "metrics.csv")
    metrics_df: pd.DataFrame()

    if os.path.exists(metrics_path):
        metrics_df = pd.read_csv(metrics_path)
    else:
        metrics_df = pd.DataFrame()

    return metrics_df


def save_patched_level(level_path: str, patcher_name: str, level: list[str]):
    tag = patcher_name.replace(" ", "_").lower()
    patched_path = level_path.replace("level", f"patched_{tag}")
    with open(patched_path, "w") as f:
        for row in level:
            f.write(row + "\n")


def calculate_eta(times: list[float], remaining: int) -> str:
    if len(times) == 0:
        return "Estimating ..."

    average = sum(times) / len(times)
    eta = remaining * average
    return time.strftime("%H:%M:%S", time.gmtime(eta))


def pipeline_repair_evaluate():
    metrics_df = read_or_create_metrics_csv()

    generators = list_generators()

    level_list = []

    print("Gathering levels...")
    for idx, generator_name in enumerate(generators):
        generator_path: str = os.path.join(os.path.curdir, "data", generator_name)

        level_files: list[str] = list_levels(generator_path)

        for level_file in level_files:
            level_list.append((level_file, generator_path))

    level_idx = 1
    level_count = len(level_list)

    print("Starting repair process...")
    start_counter = time.time()
    times = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=REPAIR_STAGE_THREADS) as executor:
        futures = [
            executor.submit(repair_level, level_path, generator_path, metrics_df)
            for level_path, generator_path in level_list
        ]

        for future in concurrent.futures.as_completed(futures):
            level_path, new_df, level_dict = future.result()

            for patcher_name, level in level_dict.items():
                save_patched_level(level_path, patcher_name, level)

            if not new_df.empty:
                metrics_df = pd.concat([metrics_df, new_df], ignore_index=True)
                metrics_df.to_csv(os.path.join(os.path.curdir, "data", "metrics.csv"), index=False)

            end_counter = time.time()
            if not new_df.empty:
                times.append(end_counter - start_counter)
            start_counter = end_counter
            level_idx += 1

            print(f"Completed level {level_idx} of {level_count} | ETA: {calculate_eta(times, level_count - level_idx)}")


start = time.time()
pipeline_repair_evaluate()
time_str = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
print(f"Fixed levels in {time_str}")
