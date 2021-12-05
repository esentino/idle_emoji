import curses
import sys
from curses import wrapper
from datetime import datetime
from math import ceil
from random import uniform
from time import sleep
from typing import List

import constants
from constants import CASH_IMAGE_MAX_DISPLAY
from emoji import Emoji
from gamesave import GameSave, load_game, save_game
from utils import row_generator, digit_generator


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
    emoji_list = [grinning_emoji, grinning_big_eyes_emoji, grinning_smiling_emoji]
    cash = game.cash
    screen.nodelay(True)
    start_time = datetime.now()
    while True:
        key = screen.getch()
        digit_gen = digit_generator()
        if key == constants.NO_KEY_PRESSED:
            old = cash
            for emoji in emoji_list:
                cash += emoji.recalculate()
            sleep(uniform(0.1, 0.3))

            if old != cash:
                refresh_display(emoji_list, cash, screen, start_time)
        else:
            for emoji in emoji_list:
                if key == ord(next(digit_gen)) and emoji.buy_price < cash:
                    cash = emoji.buy(cash)
            if key == ord(constants.EXIT_KEY):
                game = GameSave(
                    grinning_emoji.level,
                    grinning_big_eyes_emoji.level,
                    grinning_smiling_emoji.level,
                    cash,
                )
                save_game(game)
                sys.exit(0)


def display_header(screen: curses.window, row: int):
    screen.addstr(row, 0, "Emoji")
    screen.addstr(row, constants.CASH_START_COLUMN_DISPLAY, "Udział w przychodzie")
    screen.addstr(row, constants.LEVEL_START_COLUMN_DISPLAY, "Level")
    screen.addstr(row, constants.BUY_START_COLUMN_DISPLAY, "Koszt zakupu")


def refresh_display(emoji_list: List[Emoji], cash: float, screen: curses.window, start_time):
    screen.clear()
    row_gen = row_generator()

    digit_gen = digit_generator()
    zarobki = sum(emoji.production_per_second for emoji in emoji_list)
    max_zarobki = max(emoji.production_per_second for emoji in emoji_list)

    screen.addstr(next(row_gen), 0, f"kasa: {cash:.2f}")
    screen.addstr(next(row_gen), 0, f"zarobek na sekundę: {zarobki:.2f}{constants.EMOJI_CASH}/s")

    next(row_gen)
    display_header(screen, next(row_gen))

    for emoji in emoji_list:
        display_emoji(emoji, max_zarobki, screen, row=next(row_gen), key=next(digit_gen))
    next(row_gen)

    screen.addstr(next(row_gen), 0, f"Zamkniecie (wciśnij {constants.EXIT_KEY}))")

    delta = (datetime.now() - start_time).seconds or 1

    screen.addstr(next(row_gen), 0, f"{delta} - {cash/delta}")


def display_emoji(emoji: Emoji, max_zarobki: float, screen: curses.window, row: int, key: str):
    screen.addstr(row, 0, f"{emoji.image}")
    a_proportion = ceil((emoji.production_per_second * CASH_IMAGE_MAX_DISPLAY / max_zarobki))
    screen.addstr(
        row,
        constants.CASH_START_COLUMN_DISPLAY,
        f"{constants.EMOJI_CASH * a_proportion}",
    )
    screen.addstr(row, constants.LEVEL_START_COLUMN_DISPLAY, f"{emoji.level}")
    screen.addstr(row, constants.BUY_START_COLUMN_DISPLAY, f"{emoji.buy_price:.2f}")
    screen.addstr(row, constants.INFO_START_COLUMN_DISPLAY, f"dokup (wciśnij {key})")
    screen.addstr(
        row,
        constants.FUTURE_INCOME_COLUMN_DISPLAY,
        f"{emoji.production_per_second} {constants.EMOJI_ARROW_UP} {emoji.production_per_second_after_upgrade} ",
    )


wrapper(main)
