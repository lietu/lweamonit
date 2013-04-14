from time import time


class DataLogger(object):

    def __init__(self, config, logger):
        self.logger = logger

        self.sensorMap = self.get_sensor_map(config)

        logFile = config["logFile"]
        self.logger.debug("Opening log file %s" % logFile)
        self.outFile = open(logFile, "a")

    def write(self, data):
        line = ""
        for index in data:
            value = data[index]
            key = self.sensorMap[index]

            line += "\t" + key + ": " + str(value)

        line = "%i\t%s\n" % (
            time(),
            line.strip()
        )

        self.logger.debug("Writing log line")
        self.outFile.write(line)

    def get_sensor_map(self, config):
        sensorMap = dict()

        for i, item in enumerate(config["sensors"]):
            key = item["key"]

            sensorMap[i] = key

        return sensorMap
