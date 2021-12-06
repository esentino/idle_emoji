import curses
from datetime import datetime
from math import ceil
from typing import Tuple

import constants
from constants import CASH_IMAGE_MAX_DISPLAY
from emoji import Emoji
from utils import row_generator, digit_generator


def display_header(screen: curses.window, row: int):
    screen.addstr(row, 0, "Emoji")
    screen.addstr(row, constants.CASH_START_COLUMN_DISPLAY, "Udział w przychodzie")
    screen.addstr(row, constants.LEVEL_START_COLUMN_DISPLAY, "Level")
    screen.addstr(row, constants.BUY_START_COLUMN_DISPLAY, "Koszt zakupu")


def refresh_display(emoji_list: Tuple[Emoji, ...], cash: float, screen: curses.window):
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
    upgrade_product_message = (
        f"{emoji.production_per_second:.2f} {constants.EMOJI_ARROW_UP} "
        + f"{emoji.production_per_second_after_upgrade:.2f}"
    )
    screen.addstr(
        row,
        constants.FUTURE_INCOME_COLUMN_DISPLAY,
        upgrade_product_message,
    )
