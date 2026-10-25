"""
LevelManager — level definitions, progression, and completion rules.

Tracks which levels are unlocked, current level, ingredient progress within
a level, and scoring.
"""

from . import assets_config as AC


class LevelManager:
    def __init__(self):
        self.levels = dict(AC.LEVELS)
        self.current_level = 1
        self.unlocked_levels = {1}
        self.best_scores = {}      # level_id -> best score
        self.ingredients_completed = 0
        self.ingredients_total = 0
        self.level_score = 0

    def start_level(self, level_id):
        cfg = self.levels[level_id]
        self.current_level = level_id
        self.ingredients_completed = 0
        self.ingredients_total = len(cfg["ingredients"])
        self.level_score = 0

    def ingredient_completed(self, points=0):
        self.ingredients_completed += 1
        self.level_score += points

    def is_level_complete(self):
        return self.ingredients_completed >= self.ingredients_total

    def complete_level(self, time_bonus=0):
        total = self.level_score + AC.POINTS_LEVEL_BONUS + time_bonus
        prev_best = self.best_scores.get(self.current_level, 0)
        if total > prev_best:
            self.best_scores[self.current_level] = total
        # Unlock next level
        next_level = self.current_level + 1
        if next_level in self.levels:
            self.unlocked_levels.add(next_level)
        return total

    def is_unlocked(self, level_id):
        return level_id in self.unlocked_levels

    def is_final_level(self):
        return self.current_level == max(self.levels.keys())

    def get_config(self, level_id=None):
        lid = level_id or self.current_level
        return self.levels[lid]
