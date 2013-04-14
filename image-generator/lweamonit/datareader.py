import sys


class DataReader(object):

    def __init__(self, config, logger):
        self.inputFile = config["arduinoPort"]
        self.logger = logger

    def read(self):
        self.openStream()

        input = ""

        # Loop until we get good output
        while len(input) == 0:
            # Try to read a line and strip excess whitespace
            input = self.inputStream.readline(255).strip()

            # Log empty lines
            if len(input) == 0:
                self.logger.debug("Read empty line")

        self.closeStream()

        return input

    def openStream(self):
        self.logger.debug("Opening input stream")
        try:
            self.inputStream = open(self.inputFile)
            self.logger.debug(
                "Opened input stream %s " % self.inputFile
            )
        except IOError as err:
            self.logger.error(err)
            print(
                "Failed to open Arduino port (%(port)s). Please check "
                " config and permissions." % {
                    "port": self.inputFile
                }
            )

            sys.exit(1)

    def closeStream(self):
        self.logger.debug("Closing input stream")
        if self.inputStream:
            self.inputStream.close()
            self.logger.debug("... done")
        else:
            self.logger.debug("No input stream open")
