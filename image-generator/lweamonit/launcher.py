# coding=utf-8
#
# Copyright 2013 Janne Enberg

import logging
import json
import sys

from datareader import DataReader
from dataparser import DataParser
from datalogger import DataLogger
from imagereader import ImageReader
from imagedatawriter import ImageDataWriter
from runner import Runner


class Launcher(object):

    def __init__(self):
        self.logger = self.get_logger()

    def start(self):

        self.logger.debug('Starting up')

        # Read the config
        config = self.read_config()

        dataReader = DataReader(config, self.logger)
        dataParser = DataParser(config, self.logger)
        dataLogger = DataLogger(config, self.logger)
        imageReader = ImageReader(config, self.logger)
        imageDataWriter = ImageDataWriter(config, self.logger)

        runner = Runner(
            dataReader=dataReader,
            dataParser=dataParser,
            dataLogger=dataLogger,
            imageReader=imageReader,
            imageDataWriter=imageDataWriter,
            config=config,
            logger=self.logger
        )

        if len(sys.argv) > 1:
            runner.run(timestamp=int(sys.argv[1]))
        else:
            runner.run()

    def read_config(self, filename="config.json"):

        self.logger.debug("Reading config")

        # Open the configuration file
        configFile = open(filename)

        # Parse the config
        config = json.load(configFile)

        configFile.close()

        return config

    def get_logger(self):
        """Initialize the logging system"""

        logger = logging.getLogger("lweamonit")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s: %(message)s'
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        return logger
