import sys
from .ascii import fitting_ascii
from .csi import (
    fitting_sgr,
    CUU_CODE,
    SGR_8BIT_FG_COLOR_GRAY,
    SGR_8BIT_FG_COLOR_WHITE,
    SGR_8BIT_BG_COLOR_CODE,
    SGR_8BIT_BG_COLOR_BLACK,
)


def convert_frame(frame, color=True, **kwargs):
    width, height = frame.size

    rgb_frame = frame.convert(mode="RGB")
    rgb_pixels = rgb_frame.load()

    ascii_frame = []
    for y in range(height):
        line = []
        for x in range(width):
            rgb_pixel = rgb_pixels[x, y]
            # convert pixel to ascii and add fg and bg color
            if color:
                line.append(SGR_8BIT_BG_COLOR_CODE % fitting_sgr(rgb_pixel))
                line.append(SGR_8BIT_FG_COLOR_GRAY)
            line.append(fitting_ascii(rgb_pixel))
        # add return for each line
        if color:
            line.append(SGR_8BIT_BG_COLOR_BLACK)
            line.append(SGR_8BIT_FG_COLOR_WHITE)
        line.append("\n")
        ascii_frame.append("".join(line))
    return ascii_frame


def output_frame(frame, backspace=True, **kwargs):
    ascii_frame = convert_frame(frame, **kwargs)
    sys.stdout.writelines(ascii_frame)

    if backspace:
        sys.stdout.write(CUU_CODE % len(ascii_frame))
    sys.stdout.flush()
