import numpy as np
from PIL import ImageFont
from scipy.spatial import cKDTree
from .utils import cache

ASCII_VISIBLE_CHARS = [chr(i) for i in range(32, 127)]


def _char_weight(char):
    font = ImageFont.load_default()
    chr_image = font.getmask(char)
    width, height = font.getsize(char)

    black_pixels = sum(1.0 for i in np.asarray(chr_image) if i > 0)
    return black_pixels / (width * height)


def _normalize_transform(weights):
    weights_range = max(weights) - min(weights)
    return (weights - min(weights)) / weights_range


def _default_weights():
    weights = np.array([_char_weight(c) for c in ASCII_VISIBLE_CHARS])
    return _normalize_transform(weights)


DEFAULT_WEIGHTS = _default_weights()
DEFAULT_WEIGHTS_KD_TREE = cKDTree(DEFAULT_WEIGHTS.reshape(-1, 1))


@cache(key=lambda args: args[0])
def fitting_ascii(rgb_pixel):
    r, g, b = rgb_pixel
    # convert rgb to grayscale
    pixel_weight = (0.2989 * r + 0.5870 * g + 0.1140 * b) / 255
    _, index = DEFAULT_WEIGHTS_KD_TREE.query([pixel_weight])
    return ASCII_VISIBLE_CHARS[index]
