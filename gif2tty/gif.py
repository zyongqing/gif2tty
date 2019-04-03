import time
from PIL import Image, ImageSequence
from .tty import output_frame


def _fill_empty(frame):
    canvas = Image.new("RGB", frame.size, (0xFF, 0xFF, 0xFF))
    canvas.paste(frame)
    return canvas


def extract_frames(file_name, width, height, fill=False, **kwargs):
    image = Image.open(file_name)
    for frame in ImageSequence.Iterator(image):
        if fill:
            frame = _fill_empty(image)
        yield frame.resize((width, height), Image.BICUBIC)


def gif_tty(file_name, width, height, sleep=0.02, **kwargs):
    for frame in extract_frames(file_name, width, height, **kwargs):
        output_frame(frame, **kwargs)
        time.sleep(sleep)
