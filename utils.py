"""
Extra methods for displaying gui
"""


def row_generator():
    """
    Generate next value from 0
    :return:
    """
    row_number = 0
    while True:
        yield row_number
        row_number += 1


def digit_generator():
    """
    Generate next digits for 1 to 0 on keyboard. 1234567890
    :return:
    """
    for digit in "1234567890":
        yield digit
