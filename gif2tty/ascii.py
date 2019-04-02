from PIL import ImageFont
from .utils import cache


def _char_weight(char):
    font = ImageFont.load_default()
    chr_image = font.getmask(char)
    width, height = font.getsize(char)

    black_pixels = sum(
        1.0
        for y in range(height)
        for x in range(width)
        if chr_image.getpixel((x, y)) > 0
    )
    return black_pixels / (width * height)


def _linear_transform(weights):
    weights_min = min(weights.keys())
    weights_max = max(weights.keys())
    weights_range = weights_max - weights_min
    linear_weights = ((w / weights_range, c) for w, c in weights.items())
    return sorted(linear_weights)


def _default_weights():
    weights = {}
    for i in range(32, 127):
        char = chr(i)
        weights[_char_weight(char)] = char
    return _linear_transform(weights)


DEFAULT_WEIGHTS = _default_weights()


@cache(key=lambda args: args[0])
def fitting_ascii(gray_pixel):
    pixel_weight = float(gray_pixel) / 255

    previous_weight, previous_char = DEFAULT_WEIGHTS[0]
    for current_weight, current_char in DEFAULT_WEIGHTS:
        if pixel_weight <= current_weight:
            previous_euclid_distance = (pixel_weight - previous_weight) ** 2
            current_euclid_distance = (pixel_weight - current_weight) ** 2
            if current_euclid_distance >= previous_euclid_distance:
                return previous_char
            else:
                return current_char
        previous_weight, previous_char = current_weight, current_char
