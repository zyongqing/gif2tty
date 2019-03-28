#!/usr/bin/env python

from PIL import Image, ImageFont, ImageSequence
import sys
import functools
import time


DEFAULT_WIDTH = 80
DEFAULT_SLEEP = 0.0


# this function is base on
# http://code.activestate.com/recipes/580702-image-to-ascii-art-converter/
def default_weights():
    font = ImageFont.load_default()
    (chr_x, chr_y) = font.getsize(chr(32))
    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chr_y):
            for x in range(chr_x):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chr_x * chr_y))
    return weights


def cache(key):
    def decorator(func):
        _cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key(args)
            result = _cache.get(cache_key, None)

            if result is None:
                result = func(*args, **kwargs)
                _cache[cache_key] = result
            return result

        return wrapper

    return decorator


@cache(key=lambda args: args[0])
def fitting_pixel(pixel, weights):
    w = float(pixel) / 255
    wf = -1.0
    k = -1
    for i in range(len(weights)):
        if abs(weights[i] - w) <= abs(wf - w):
            wf = weights[i]
            k = i
    return chr(k + 32)


def extract_frame(file_name, fill_empty=False):
    im = Image.open(file_name)
    for frame in ImageSequence.Iterator(im):
        if fill_empty:
            canvas = Image.new("RGBA", frame.size, (0xFF, 0xFF, 0xFF, 0xFF))
            canvas.paste(frame)
            yield canvas
        else:
            yield frame


def convert_frame(frame, weights, width=80):
    height = width // 2
    resize_frame = frame.resize((width, height), Image.BICUBIC)
    gray_frame = resize_frame.convert("L")
    all_pixels = gray_frame.load()

    ascii_frame = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(fitting_pixel(all_pixels[x, y], weights))
        line.append("\n")
        ascii_frame.append("".join(line))
    return ascii_frame


def output_frame(frame, backspace=True):
    sys.stdout.writelines(frame)
    sys.stdout.flush()

    if backspace:
        sys.stdout.write("\033[F" * len(frame))
        sys.stdout.flush()


def print_gif(
    file_name, width=DEFAULT_WIDTH, fill_empty=False, sleep=DEFAULT_SLEEP, weights=None
):
    if weights is None:
        weights = default_weights()
    for frame in extract_frame(file_name, fill_empty):
        ascii_frame = convert_frame(frame, weights, width=width)
        output_frame(ascii_frame)
        time.sleep(sleep)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="gif_console", description="show gif in console mode"
    )
    parser.add_argument("filename", help="gif name")
    parser.add_argument("--width", help="width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--sleep", help="sleep time", type=float, default=DEFAULT_SLEEP)
    parser.add_argument("--fill", help="fill empty", action="store_true")
    args = parser.parse_args()
    try:
        print_gif(
            args.filename, width=args.width, sleep=args.sleep, fill_empty=args.fill
        )
    except Exception as e:
        print(e)
