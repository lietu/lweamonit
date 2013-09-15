# coding=utf-8
#
# Copyright 2013 Janne Enberg

from PIL import Image
import urllib2 as urllib
import io


class ImageReader(object):

    def __init__(self, config, logger):
        self.logger = logger
        self.url = config["imageSource"]

    def read(self):
        self.logger.debug("Reading image from %s" % self.url)
        fd = urllib.urlopen(self.url)
        image_file = io.BytesIO(fd.read())
        return Image.open(image_file)
