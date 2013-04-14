import re


class DataParser(object):

    def __init__(self, config, logger):
        self.sensorMap = self.get_sensor_map(config)
        self.test = re.compile("([a-zA-Z0-9]+: ?[0-9.]+\|?)+")

    def parseLine(self, line):
        if not self.test.match(line):
            return None

        result = dict()
        for sensor in line.split("|"):
            tmp = sensor.split(":")

            key = tmp[0].strip()
            value = float(tmp[1].strip())

            index = self.sensorMap[key]

            result[index] = value

        return result

    def get_sensor_map(self, config):
        sensorMap = dict()

        for i, item in enumerate(config["sensors"]):
            key = item["key"]

            sensorMap[key] = i

        return sensorMap
