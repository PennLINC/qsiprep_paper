from PIL import Image
from glob import glob

TILE_SIZE = 256
positions = {
    "abcd": {
        "double": (2400, 360),
        "single": (2600, 440),
        "triple": (1500, 650)
    },
    "pnc": {
        ""
    }
}


def extract_squares(image, out_file, scheme="abcd"):
    no_crossing = positions[scheme]['single']
    no_crossing_rect = (no_crossing[0], no_crossing[1],
                        no_crossing[0] + TILE_SIZE,
                        no_crossing[1] + TILE_SIZE)
    one_crossing = positions[scheme]['double']
    one_crossing_rect = (one_crossing[0], one_crossing[1],
                         one_crossing[0] + TILE_SIZE,
                         one_crossing[1] + TILE_SIZE)
    two_crossing = positions[scheme]['triple']
    two_crossing_rect = (two_crossing[0], two_crossing[1],
                         two_crossing[0] + TILE_SIZE,
                         two_crossing[1] + TILE_SIZE)
    in_image = Image.open(image)
    out_image = Image.new('RGB', (TILE_SIZE * 3, TILE_SIZE))

    no_crossing_image = in_image.crop(no_crossing_rect)
    out_image.paste(no_crossing_image, (0, 0))
    one_crossing_image = in_image.crop(one_crossing_rect)
    out_image.paste(one_crossing_image, (TILE_SIZE, 0))
    two_crossing_image = in_image.crop(two_crossing_rect)
    out_image.paste(two_crossing_image, (TILE_SIZE * 2, 0))
    out_image.save(out_file)


schemes = ["pnc", "abcd", "crash", "q7"]
recons = ["GQIODF", "wmFOD", "MAPLMRIODF"]
for scheme in schemes:
    for suffix in recons:
        images = glob("odf_figs/odfs/{scheme}*{suffix}*".format(scheme=scheme, suffix=suffix))
        if not images:
            continue
        image = sorted(images)[0]
        extract_squares(image, scheme + "_" + suffix + ".png")

import os.path as op
PADDING = 32
WIDTH = (PADDING + TILE_SIZE * 3)
HEIGHT = (TILE_SIZE + PADDING)
mosaic_image = Image.new('RGB', (WIDTH * len(recons), HEIGHT * len(schemes)))
for schemenum, scheme in enumerate(schemes):
    for reconnum, recon in enumerate(recons):
        img_path = scheme + "_" + recon + ".png"
        if not op.exists(img_path):
            print(scheme, recon, "missing")
            continue
        top = HEIGHT * schemenum + PADDING // 2
        left = WIDTH * reconnum + PADDING // 2
        mosaic_image.paste(Image.open(img_path), (left, top))
mosaic_image.save("mosaic.png")



def extract_square(image, square_type, scheme="abcd"):
    position = {
        "single": (0, 0),
        "crossing": (TILE_SIZE, 0),
        "double": (TILE_SIZE * 2, 0)
    }[square_type]
    rect = (position[0], position[1],
            position[0] + TILE_SIZE,
            position[1] + TILE_SIZE)
    in_image = Image.open(image)

    return in_image.crop(rect)


WIDTH = HEIGHT = (PADDING + TILE_SIZE)
def fiber_type_image(fiber_type):
    _image = Image.new('RGB', (WIDTH * len(recons), HEIGHT * len(schemes)))
    for schemenum, scheme in enumerate(schemes):
        for reconnum, recon in enumerate(recons):
            img_path = scheme + "_" + recon + ".png"
            if not op.exists(img_path):
                print(scheme, recon, "missing")
                continue
            top = HEIGHT * schemenum + PADDING // 2
            left = WIDTH * reconnum + PADDING // 2
            _image.paste(extract_square(img_path, fiber_type), (left, top))
    _image.save(fiber_type + "_fiber.png")
fiber_type_image("single")
fiber_type_image("crossing")
fiber_type_image("double")
