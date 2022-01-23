import curses
import sys
from datetime import datetime
from random import uniform
from time import sleep

from . import constants
from .display import refresh_display
from .emoji import Emoji
from .save import load_game, Save, save_game
from .utils import digit_generator


def main(screen: curses.window):
    curses.noecho()
    game = load_game()
    grinning_emoji = Emoji(
        "first", constants.EMOJI_GRINNING_FACE, 3.738, 1.67, 1.07, 0.6, game.a_level
    )
    grinning_big_eyes_emoji = Emoji(
        "second", constants.EMOJI_GRINNING_FACE_BIG_EYES, 60, 20, 1.15, 3, game.b_level
    )
    grinning_smiling_emoji = Emoji(
        "third",
        constants.EMOJI_GRINNING_FACE_SMILING_EYES,
        720,
        90,
        1.14,
        6,
        game.c_level,
    )
    emoji_list = (grinning_emoji, grinning_big_eyes_emoji, grinning_smiling_emoji)
    cash = game.cash
    screen.nodelay(True)
    while True:
        key = screen.getch()
        digit_gen = digit_generator()
        if key == constants.NO_KEY_PRESSED:
            old = cash
            for emoji in emoji_list:
                cash += emoji.recalculate(datetime.now())
            sleep(uniform(0.1, 0.3))

            if old != cash:
                refresh_display(emoji_list, cash, screen)
        else:
            for emoji in emoji_list:
                if key == ord(next(digit_gen)) and emoji.buy_price < cash:
                    cash = emoji.buy(cash)
            if key == ord(constants.EXIT_KEY):
                game = Save(
                    *[a.level for a in emoji_list],
                    cash,
                )
                save_game(game)
                sys.exit(0)