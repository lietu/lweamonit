import time


class Runner(object):
    def __init__(self, dataReader, dataParser, dataLogger, imageReader,
                 imageDataWriter, config, logger):
        self.dataReader = dataReader
        self.dataParser = dataParser
        self.dataLogger = dataLogger
        self.imageReader = imageReader
        self.imageDataWriter = imageDataWriter
        self.imageFile = config["imageFile"]
        self.iterationInterval = config["iterationInterval"]
        self.logger = logger

    def run(self, timestamp=None):
        breakAfterFirst = False
        if timestamp is not None:
            breakAfterFirst = True

        i = 0
        while True:
            i += 1
            self.logger.debug("Starting iteration %i" % i)

            startTime = time.time()
            image = self.imageReader.read()

            data = None
            while data is None:
                data = self.dataParser.parseLine(self.dataReader.read())

            self.dataLogger.write(data, timestamp=timestamp)
            self.imageDataWriter.write(data, image)

            image.save(self.imageFile, "JPEG")

            endTime = time.time()
            timeElapsed = endTime - startTime
            self.logger.info("Generated image in %.4f seconds" % timeElapsed)
            self.logger.info("Data was: " + str(data))

            if self.iterationInterval == 0 or breakAfterFirst is True:
                break

            sleepSeconds = self.iterationInterval - timeElapsed

            self.logger.debug("Sleeping for %.2f seconds" % sleepSeconds)

            time.sleep(sleepSeconds)
