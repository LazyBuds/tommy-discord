
from math import floor
import os

# TODO: Chop long single-words
# from PIL import ImageFont
from PIL import Image, ImageFont

def wrap(font, text, line_width):
    words = text.split()

    lines = []
    line = []

    for word in words:
        newline = ' '.join(line + [word])

        w, h = font.getsize(newline)

        if w > line_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)

    if line:
        lines.append(' '.join(line))

    return ('\n'.join(lines)).strip()


def auto_text_size(text, font, desired_width, fallback_size=75, font_scalar=1):
    for size in range(42, 80):
        new_font = font.font_variant(size=floor(size * font_scalar))
        font_width, _ = new_font.getsize(text)
        if font_width >= desired_width:
            wrapped = wrap(new_font, text, desired_width)
            w = max(new_font.getsize(line)[0] for line in wrapped.splitlines())
            if abs(desired_width - w) <= 10:
                return new_font, wrapped

    fallback = font.font_variant(size=fallback_size)
    return fallback, wrap(fallback, text, desired_width)


def auto_size(text, font, desired_width, fallback_size=96, font_scalar=1):
    for size in range(60, 100):
        new_font = font.font_variant(size=floor(size * font_scalar))
        font_width, _ = new_font.getsize(text)
        if font_width >= desired_width:
            wrapped = wrap(new_font, text, desired_width)
            w = max(new_font.getsize(line)[0] for line in wrapped.splitlines())
            if abs(desired_width - w) <= 10:
                return new_font, wrapped

    fallback = font.font_variant(size=fallback_size)
    return fallback, wrap(fallback, text, desired_width)

