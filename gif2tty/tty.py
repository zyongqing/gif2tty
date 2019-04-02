import sys
from .ascii import fitting_ascii
from .csi import fitting_sgr, CUU_CODE, SGR_8BIT_BG_COLOR_BLACK, SGR_8BIT_FG_COLOR_WHITE


def convert_frame(frame):
    width, height = frame.size

    rgb_frame = frame.convert(mode="RGB")
    rgb_pixels = rgb_frame.load()

    gray_frame = frame.convert(mode="L")
    gray_pixels = gray_frame.load()

    ascii_frame = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(fitting_sgr(rgb_pixels[x, y]))
            line.append(fitting_ascii(gray_pixels[x, y]))
        line.append(SGR_8BIT_BG_COLOR_BLACK)
        line.append(SGR_8BIT_FG_COLOR_WHITE)
        line.append("\n")
        ascii_frame.append("".join(line))
    return ascii_frame


def output_frame(frame, backspace=True):
    ascii_frame = convert_frame(frame)
    sys.stdout.writelines(ascii_frame)

    if backspace:
        sys.stdout.write(CUU_CODE % len(ascii_frame))
    sys.stdout.flush()
