import numpy as np
import py4j.java_gateway

from patching.metrics.metric import Metric
from utils.token_defs import *


class Difficulty(Metric):
    def __init__(self):
        self.original_difficulty: float = 0.0
        self.generated_difficulty: float = 0.0

    def pre_hook(
        self,
        original_level: list[str],
        original_mario_result: py4j.java_gateway.JavaObject,
        generated_level: list[str],
        generated_mario_result: py4j.java_gateway.JavaObject,
    ):
        self.original_difficulty = difficulty(original_level, original_mario_result)
        self.generated_difficulty = difficulty(generated_level, generated_mario_result)

    def iter_hook(
        self,
        mario_result: py4j.java_gateway.JavaObject,
        fixed_level: list[str],
    ):
        pass

    def post_hook(
            self,
            mario_result: py4j.java_gateway.JavaObject,
            original_level: list[str],
            generated_level: list[str],
            fixed_level: list[str],
    ):
        return {
            "Difficulty original": self.original_difficulty,
            "Difficulty generated": self.generated_difficulty,
            "Difficulty fixed": difficulty(fixed_level, mario_result)
        }


def difficulty(level: list[str], mario_result: py4j.java_gateway.JavaObject) -> float:
    """
    Consists of a static and a dynamic evaluation.
    Static evaluation is based on data gathered by analysing the level itself.
    Dynamic evaluation is based on data gathered by the Mario AI Framework agent playing the level
    :param level: Level to analyse
    :param mario_result: Data gathered by the AI agent, type is MarioResult (see Mario AI Framework)
    :return: Difficulty score, higher meaning more difficult
    """
    # Static evaluation

    # Convert level to numpy ndarray
    level = np.array([list(row) for row in level])

    # Determine the height for every vertical column
    width: int = level.shape[1]
    heights: list[int] = [0] * width

    for column in range(width):
        # Move down the column until we find a non "-" character
        for row in range(level.shape[0]):
            if level[row][column] != "-":
                heights[column] = level.shape[0] - row
                break

    # Iterate all vertical columns
    current_gap_width: int = 0

    static_gap_widths = []
    enemy_count: int = 0
    cannon_count: int = 0
    tube_count: int = 0
    powerup_count: int = 0

    for column in range(width - 1):
        if heights[column] == 0:
            current_gap_width += 1
        else:
            if current_gap_width > 0:
                static_gap_widths.append(current_gap_width)
                current_gap_width = 0

        enemy_count += count_enemies(level[:, column])
        cannon_count += count_cannon(level[:, column])
        tube_count += count_tubes((level[:, column], level[:, column + 1]))
        powerup_count += count_powerups(level[:, column])

    # Dynamic evaluation

    # Find the gaps mario *actually* jumped over
    # 10 is the maximum gap width mario can handle
    # 5 is the highest mario can jump
    jumps = mario_result.getJumps()
    dynamic_gap_widths = []
    for jump in jumps:
        y_start = int(jump.getStart().getMarioY() / 16)
        y_end = int(jump.getEnd().getMarioY() / 16) - 1

        y_pos = y_start - 3 if y_start > y_end else y_end - 5

        x_start = max(int(jump.getStart().getMarioX() / 16) - 1, 0)
        x_end = min(int(jump.getEnd().getMarioX() / 16) + 1, width)

        # Check downwards from all mario positions during the jump
        # to check if he's jumping an actual gap
        gap_length = 0
        for x in range(x_start, x_end):
            is_gap = True
            for y in range(y_pos, level.shape[0]):
                if level[y][x] not in NON_BLOCKS:
                    is_gap = False
                    break
                level[y][x] = "x"

            if is_gap:
                gap_length += 1
            else:
                if gap_length > 0:
                    dynamic_gap_widths.append(gap_length)
                    gap_length = 0

    hurts = mario_result.getMarioNumHurts()
    fall_kills = mario_result.getKillsByFall()
    collected_powerups = \
        mario_result.getCurrentLives() \
        + mario_result.getNumCollectedMushrooms() \
        + mario_result.getNumCollectedFireflower()

    static_gap_avg = sum(static_gap_widths) / (1 + len(static_gap_widths))
    dynamic_gap_avg = sum(dynamic_gap_widths) / (1 + len(dynamic_gap_widths))

    score = static_gap_avg * 1.2 \
        + dynamic_gap_avg * 1.428 \
        + (enemy_count - hurts - fall_kills) * 0.02 \
        + fall_kills * 0.333 \
        + hurts * 1.5 \
        + tube_count * 0.1 \
        + cannon_count * 0.333 \
        - (powerup_count - collected_powerups) * 0.2 \
        - collected_powerups * 2.0

    return score


def count_enemies(column: np.ndarray) -> int:
    # Count enemies in a column
    enemies: int = 0
    for row in range(column.shape[0]):
        if column[row] in [GOOMBA, KOOPA, FLYING_KOOPA, SPINY]:
            enemies += 1
    return enemies


def count_cannon(column: np.ndarray) -> int:
    # Count cannon in a column
    # Can at most be 2 per column
    cannon: int = 0
    reached: int = 0

    for row in range(column.shape[0]):
        if column[row] == CANNON:
            cannon += 1
            reached = row
            break

    # Bullet bill cannons can be stacked, which is indicated by a "B" in the column below the '*' characters
    for r2 in range(reached, column.shape[0]):
        if column[r2] == CANNON_BASE:
            cannon += 1
            break

    return cannon


def count_tubes(columns: tuple[np.ndarray, np.ndarray]) -> int:
    # Receives two columns, since tubes are 2 blocks wide and we dont want to count them twice
    # Can at most be 1 per 2-pair of columns
    tubes: int = 0
    for row in range(columns[0].shape[0]):
        if columns[0][row] == FLOWER_TUBE and columns[1][row] == FLOWER_TUBE:
            tubes += 1
            break

    return tubes


def count_powerups(column: np.ndarray) -> int:
    # Count powerups in a column
    powerups: int = 0
    for row in range(column.shape[0]):
        if column[row] in [QUESTION_LEVEL_UP, BRICK_LEVEL_UP, HIDDEN_ONE_UP, BRICK_ONE_UP]:
            powerups += 1
    return powerups
