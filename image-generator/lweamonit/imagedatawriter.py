from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont


class ImageDataWriter(object):

    def __init__(self, config, logger):
        self.logger = logger
        self.sensors = config["sensors"]

        self.bgColor = ImageColor.getrgb(config["legendColor"])
        self.outlineColor = ImageColor.getrgb(config["outlineColor"])
        self.textColor = ImageColor.getrgb(config["textColor"])

        self.font = ImageFont.truetype(config["font"], config["fontSize"])

    def write(self, data, image):
        self.logger.debug("Drawing data on image")
        draw = ImageDraw.Draw(image)

        self.draw_legend(draw, data)

        self.draw_sensors(draw, data)

    def get_sensor_color(self, index):
        if "ImageColor" not in self.sensors[index]:
            color = ImageColor.getrgb(
                self.sensors[index]["color"]
            )
            self.sensors[index]["ImageColor"] = color

        return self.sensors[index]["ImageColor"]

    def draw_legend(self, draw, data):
        """Draw the legend"""

        # Draw the background
        draw.rectangle(
            [(2, 2), (300, 26)],
            outline=self.outlineColor,
            fill=self.bgColor
        )

        for index in data:
            value = data[index]
            sensor = self.sensors[index]

            sensorColor = self.get_sensor_color(index)

            draw.rectangle(
                [(6, 6), (22, 22)],
                outline=self.outlineColor,
                fill=sensorColor
            )

            draw.text(
                (26, 7),
                "%s (%.2f %s)" % (
                    sensor["name"],
                    float(value),
                    sensor["unit"]
                ),
                fill=self.textColor,
                font=self.font
            )

    def draw_sensors(self, draw, data):
        """Draw all the sensors' charts"""

        for index in data:
            value = data[index]
            sensor = self.sensors[index]

            sensorColor = self.get_sensor_color(index)

            self.draw_bar_chart(
                draw=draw,
                rangeMin=min(sensor["range"]),
                rangeMax=max(sensor["range"]),
                unit=sensor["unit"],
                value=value,
                top=30,
                left=2,
                width=64,
                height=100,
                spacing=4,
                color=sensorColor
            )

    def draw_bar_chart(self, draw, rangeMin, rangeMax, unit, value,
                       top, left, width, height, spacing, color):
        """Draw a bar chart on the image"""

        textSpacing = 6

        # Calculate other useful numbers
        rangeMid = abs(rangeMin) - rangeMax
        bottom = top + height
        right = left + width

        # Make sure we stay inside our bounding box for this
        if value > rangeMax:
            value = rangeMax

        if value < rangeMin:
            value = rangeMin

        # Draw the container box
        draw.rectangle(
            [(left, top), (right, bottom)],
            outline=self.outlineColor,
            fill=self.bgColor
        )

        # Calculate area for displaying the bar
        areaTop = top + spacing
        areaLeft = left + spacing
        areaBottom = bottom - spacing
        areaRight = left + 8
        areaHeight = areaBottom - areaTop

        # Draw container for the bar
        draw.rectangle(
            [
                (areaLeft, areaTop),
                (areaRight, areaBottom)
            ],
            outline=self.outlineColor,
            fill=self.bgColor
        )

        # Draw max, mid and min point values
        self.draw_text(
            draw,
            (areaRight + textSpacing, areaTop),
            str(rangeMax) + " " + unit
        )

        self.draw_text(
            draw,
            (
                areaRight + textSpacing,
                areaTop + (height / 2)
            ),
            str(rangeMid) + " " + unit,
            align="middle"
        )

        self.draw_text(
            draw,
            (areaRight + textSpacing, areaBottom),
            str(rangeMin) + " " + unit,
            align="bottom"
        )

        # Calculation of bar height
        heightRange = abs(rangeMin - rangeMax)
        heightRatio = float(areaHeight) / heightRange
        adjustedValue = abs(rangeMin) + float(value)
        valueHeight = int(adjustedValue * heightRatio)
        valueTop = areaBottom - valueHeight

        draw.rectangle(
            [
                (areaLeft + 1, valueTop),
                (areaRight - 1, areaBottom)
            ],
            fill=color
        )

    def draw_text(self, draw, position, text, align="top"):
        """Draw text with position and alignment"""

        yOffset = self.get_align_offset(draw, text, align)

        draw.text(
            (
                position[0],
                position[1] + yOffset
            ),
            text,
            font=self.font,
            fill=self.textColor
        )

    def get_align_offset(self, draw, text, align):
        """Get the Y offset to apply to align text's edge to given position"""

        if align == "top":
            return 0

        textSize = draw.textsize(text, font=self.font)

        if align == "bottom":
            return textSize[1] * -1
        elif align == "middle":
            return ((textSize[1] / 2) * -1) - 2

        raise ValueError("Invalid value for 'align'")
