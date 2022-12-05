import re


def clean_console_color_code(text):
    return re.sub(r'\033\[(\d+(;\d+)?)?m', '', text)
