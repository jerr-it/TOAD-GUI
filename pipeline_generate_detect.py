"""
Generates unplayable levels for all generators.
"""

import concurrent.futures
import os

from py4j.java_gateway import JavaGateway

from patching import GENERATE_STAGE_THREADS
from utils.toad_gan_utils import load_trained_pyramid, generate_sample, TOADGAN_obj
from utils.level_utils import one_hot_to_ascii_level, place_a_mario_token

MARIO_AI_PATH = os.path.abspath(os.path.join(os.path.curdir, "Mario-AI-Framework/mario-1.0-SNAPSHOT.jar"))

LEVEL_WIDTH = 202
LEVEL_HEIGHT = 16
LEVELS_PER_GENERATOR = 100


def list_generators() -> list[str]:
    """
    Lists all generators.
    :return: List of generator names.
    """
    base_path: str = os.path.join(os.path.curdir, "generators", "v2")
    sub_folders: list[str] = os.listdir(base_path)

    directories = []
    for sub_folder in sub_folders:
        directories.append(os.path.join(base_path, sub_folder))

    return directories


def load_generator(path: str) -> TOADGAN_obj:
    """
    Loads the generator from the given path.
    :param path: Path to the generator.
    :return: Generator object.
    """
    return load_trained_pyramid(path)[0]


def generate_unplayable_levels(generator: TOADGAN_obj, num: int, generator_path: str, verbose: bool = False):
    """
    Generates unplayable levels.
    :param num: Number of levels to generate.
    :param generator: Generator to use.
    :param generator_path: File path to the generator.
    :param verbose: True if the progress should be printed to the console.
    :return: Unplayable level.
    """
    gateway = JavaGateway.launch_gateway(
        classpath=MARIO_AI_PATH,
        die_on_exit=True,
    )

    game = gateway.jvm.engine.core.MarioGame()
    agent = gateway.jvm.agents.robinBaumgarten.Agent()

    scl_h = LEVEL_HEIGHT / generator.reals[-1].shape[-2]
    scl_w = LEVEL_WIDTH / generator.reals[-1].shape[-1]

    unplayable_level_count = 0
    total_level_count = 0

    for i in range(num):
        if verbose:
            print(f"Generating level {i + 1}/{num} for {generator_path}")

        ascii_level: list[str] = []
        progress: float = 1.0

        while 1.0 - progress < 0.01:
            level, scales, noises = generate_sample(
                generator.Gs, generator.Zs, generator.reals,
                generator.NoiseAmp, generator.num_layers, generator.token_list,
                scale_h=scl_w, scale_v=scl_h
            )

            total_level_count += 1

            ascii_level = one_hot_to_ascii_level(level, generator.token_list)
            ascii_level = place_a_mario_token(ascii_level)

            progress = evaluate_level(game, agent, ascii_level)

        unplayable_level_count += 1

        save_generated_level(ascii_level, progress, generator_path, i)

    # Write the number of unplayable levels to a file
    with open(os.path.join(os.path.curdir, "data", "unplayable_levels_quote.txt"), "a") as f:
        f.write(f"{generator_path}: {unplayable_level_count}/{total_level_count}, {unplayable_level_count/total_level_count}\n")

    gateway.java_process.kill()
    gateway.shutdown()


def save_generated_level(level: list[str], progress: float, generator_path: str, number: int = 0):
    """
    Saves the generated level to a file.
    :param level: Generated level.
    :param progress: Progress of the level. Saves time later on.
    :param generator_path: Path to the generator.
    :param number: Number of the level.
    :return: None
    """
    generator_name = os.path.basename(generator_path)

    level_path = os.path.join(os.path.curdir, "data", generator_name)
    os.makedirs(level_path, exist_ok=True)

    level_name = f"level_{generator_name}_{number}.txt"
    level_path = os.path.join(level_path, level_name)

    with open(level_path, "w") as f:
        f.write(f"{progress}\n")
        for row in level:
            f.write(row)


def evaluate_level(game, agent, level: list[str]) -> float:
    """
    Evaluates the level.
    :param game: JavaGateway object of the Mario game.
    :param agent: JavaGateway object of the agent.
    :param level: Super Mario level defined as a list of strings. (Row-wise)
    :return: Progress in %
    """
    # TODO find solution for agent getting stuck in a loop because of high walls. Waiting 10 seconds per
    #  unplayable level is not a good solution
    result = game.runGame(agent, ''.join(level), 20)
    progress = result.getCompletionPercentage()

    return progress


def pipeline_generate():
    with concurrent.futures.ThreadPoolExecutor(max_workers=GENERATE_STAGE_THREADS) as executor:
        futures = [
            executor.submit(
                generate_unplayable_levels,
                load_generator(generator_path),
                LEVELS_PER_GENERATOR,
                generator_path,
                verbose=True)
            for generator_path in list_generators()
        ]

        for future in concurrent.futures.as_completed(futures):
            pass


pipeline_generate()
