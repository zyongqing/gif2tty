import time
from PIL import Image, ImageSequence
from .ascii import fitting_pixel
from .tty import write_lines, move_up
from .weight import DEFAULT_WEIGHTS


def _extract_frames(file_name, fill_empty=False):
    im = Image.open(file_name)
    for frame in ImageSequence.Iterator(im):
        if fill_empty:
            canvas = Image.new("RGBA", frame.size, (0xFF, 0xFF, 0xFF, 0xFF))
            canvas.paste(frame)
            yield canvas
        else:
            yield frame


def _convert_frame(frame, width, height, weights):
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


def _tty_frame(frame, width, height, weights=DEFAULT_WEIGHTS, backspace=True):
    ascii_frame = _convert_frame(frame, width, height, weights)
    write_lines(ascii_frame)
    if backspace:
        move_up(len(ascii_frame))


def tty_gif(file_name, width, height, sleep, fill_empty=False):
    for frame in _extract_frames(file_name, fill_empty):
        _tty_frame(frame, width, height)
        time.sleep(sleep)
