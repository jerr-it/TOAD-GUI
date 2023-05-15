from patching.metrics.coins import Coins
from patching.metrics.collected_mushrooms import CollectedMushrooms
from patching.metrics.difficulty import DifficultyOriginal, DifficultyGenerated, DifficultyFixed
from patching.metrics.hits import Hits
from patching.metrics.jump_air_time import JumpAirTime
from patching.metrics.jump_length import JumpLength
from patching.metrics.jumps import Jumps
from patching.metrics.lives import Lives
from patching.metrics.memory import Memory
from patching.metrics.pattern_variation import PatternVariationOriginal, PatternVariationGenerated, PatternVariationFixed
from patching.metrics.remaining_time import RemainingTime
from patching.metrics.runtime import Runtime
from patching.metrics.total_kills import TotalKills
from patching.metrics.tpkl import TPKLOriginalGenerated, TPKLOriginalFixed
from patching.metrics.tries import Tries

metrics = [
    {"name": "TPKL Original Generated", "unit": "", "object": TPKLOriginalGenerated()},
    {"name": "TPKL Original Fixed", "unit": "", "object": TPKLOriginalFixed()},
    {"name": "Pattern Variation Original", "unit": "", "object": PatternVariationOriginal()},
    {"name": "Pattern Variation Generated", "unit": "", "object": PatternVariationGenerated()},
    {"name": "Pattern Variation Fixed", "unit": "", "object": PatternVariationFixed()},
    {"name": "Tries", "unit": "", "object": Tries()},
    {"name": "Difficulty Original", "unit": "", "object": DifficultyOriginal()},
    {"name": "Difficulty Generated", "unit": "", "object": DifficultyGenerated()},
    {"name": "Difficulty Fixed", "unit": "", "object": DifficultyFixed()},
    {"name": "Remaining time", "unit": "s", "object": RemainingTime()},
    {"name": "Total kills", "unit": "", "object": TotalKills()},
    {"name": "Coins", "unit": "", "object": Coins()},
    {"name": "Jumps", "unit": "", "object": Jumps()},
    {"name": "Hits", "unit": "", "object": Hits()},
    {"name": "Collected mushrooms", "unit": "", "object": CollectedMushrooms()},
    {"name": "Lives", "unit": "", "object": Lives()},
    {"name": "Max jump length", "unit": "", "object": JumpLength()},
    {"name": "Max jump air time", "unit": "", "object": JumpAirTime()},
    {"name": "Memory", "unit": "B", "object": Memory()},
    {"name": "Runtime", "unit": "s", "object": Runtime()}
]
