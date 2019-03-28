from PIL import ImageFont


# this function is base on
# http://code.activestate.com/recipes/580702-image-to-ascii-art-converter/
def _default_weights():
    font = ImageFont.load_default()
    (chr_x, chr_y) = font.getsize(chr(32))
    weights = []
    for i in range(32, 127):
        chr_image = font.getmask(chr(i))
        ctr = 0
        for y in range(chr_y):
            for x in range(chr_x):
                if chr_image.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chr_x * chr_y))
    return weights


DEFAULT_WEIGHTS = _default_weights()
