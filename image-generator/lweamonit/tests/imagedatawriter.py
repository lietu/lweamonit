# coding=utf-8
#
# Copyright 2013 Janne Enberg

import os
import sys
import inspect
from PIL import Image


def setup_path():
    currentdir = os.path.dirname(
        os.path.abspath(
            inspect.getfile(inspect.currentframe())
        )
    )

    parentdir = os.path.dirname(currentdir)
    parentdir = os.path.dirname(parentdir)

    sys.path.append(parentdir)


def run_test(infile, outfile):

    setup_path()

    from lweamonit.imagedatawriter import ImageDataWriter
    from lweamonit.launcher import Launcher

    data = [
        1050,
        34.55,
        -35,
        22.3
    ]

    launcher = Launcher()

    logger = launcher.logger
    config = launcher.read_config("config.json")

    idw = ImageDataWriter(
        config,
        logger
    )

    image = Image.open(infile)

    idw.write(data, image)

    image.save(outfile, "JPEG", quality=88, optimize=True, progressive=True)

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]

    run_test(infile, outfile)
