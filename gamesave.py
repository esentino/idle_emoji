import json
from dataclasses import dataclass, field
from datetime import datetime

import constants
from constants import SAVE_GAME_FILE


@dataclass
class GameSave:
    a_level: int = 1
    b_level: int = 0
    c_level: int = 0
    cash: float = 0.0
    time: datetime = field(default_factory=lambda: datetime.now())


def load_game() -> GameSave:
    try:
        with open(SAVE_GAME_FILE) as file:
            data = json.load(file)
    except FileNotFoundError:
        return GameSave()
    return GameSave(
        data["a"],
        data["b"],
        data["c"],
        data["cash"],
        datetime.strptime(data["time"], constants.DATETIME_FORMAT),
    )


def save_game(game: GameSave):
    with open(SAVE_GAME_FILE, "w") as file:
        response = {
            "a": game.a_level,
            "b": game.b_level,
            "c": game.c_level,
            "cash": game.cash,
            "time": game.time.strftime(constants.DATETIME_FORMAT),
        }
        file.write(json.dumps(response))
