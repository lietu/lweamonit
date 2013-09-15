# coding=utf-8
#
# Copyright 2013 Janne Enberg

from PIL import ImageDraw
from PIL import ImageColor
from PIL import ImageFont
from datetime import datetime
from dateutil.tz import tzlocal

from lweamonit.utils import cached_method


class ImageDataWriter(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def write(self, data, image):
        self.logger.debug("Drawing data on image")

        x, y = 16, 16

        legendSpacing = 16

        legend = Legend(
            data,
            self.config
        )

        legend.draw(
            x,
            y,
            image
        )

        w, h = legend.get_size()

        y += h + legendSpacing

        sensors = Sensors(
            data,
            self.config
        )

        sensors.draw(
            x,
            y,
            image
        )

        date = DateBox(self.config)

        w, h = date.get_size()

        imageWidth, imageHeight = image.size
        x = imageWidth - w - legendSpacing
        y = 16

        date.draw(x, y, image)


class Rectangle(object):
    def __init__(self, width, height, outline, fill=None):
        self.width = width
        self.height = height

        if outline:
            self.outline = ImageColor.getrgb(outline)
        else:
            self.outline = None

        if fill:
            self.fill = ImageColor.getrgb(fill)
        else:
            self.fill = None

    def get_size(self):
        return self.width, self.height

    def draw(self, x, y, image):
        draw = ImageDraw.Draw(image)

        coordinates = [
            (x, y),
            (x + self.width, y + self.height)
        ]

        draw.rectangle(
            coordinates,
            fill=self.fill,
            outline=self.outline
        )


class Text(object):
    def __init__(self, text, config, font=None, fontSize=None):
        if font is None:
            font = config["font"]
        if fontSize is None:
            fontSize = config["fontSize"]

        self.text = text
        self.font = ImageFont.truetype(font, fontSize)
        self.color = ImageColor.getrgb(config["textColor"])

    def get_size(self):
        return self.font.getsize(self.text)

    def draw(self, x, y, image, valign="middle"):
        if valign:
            yOffset = self.get_valign_offset(valign)
            y += yOffset

        draw = ImageDraw.Draw(image)
        draw.text([x, y], self.text, font=self.font, fill=self.color)

    def get_valign_offset(self, valign):
        """Get the Y offset to apply to align text's edge to given position"""

        if valign == "top":
            return 0

        textSize = self.get_size()

        if valign == "bottom":
            return textSize[1] * -1
        elif valign == "middle":
            return ((textSize[1] / 2) * -1)

        raise ValueError("Invalid value for 'valign'")


class DateBox(object):
    def __init__(self, config):
        tz = tzlocal()
        dateFormat = '%Y-%m-%d %H:%M:%S UTC%z'
        self.textContent = datetime.now(tz).strftime(dateFormat)
        self.font = config["dateFont"]
        self.fontSize = config["dateFontSize"]
        self.config = config

        self.padding = 8

    @cached_method
    def get_size(self):
        text = self.get_text()

        w, h = text.get_size()

        w, h = w + self.padding * 2, h + self.padding * 2

        return w, h

    def draw(self, x, y, image):
        w, h = self.get_size()

        rect = Rectangle(
            w,
            h,
            self.config["outlineColor"],
            self.config["legendColor"]
        )

        rect.draw(x, y, image)

        x, y = x + self.padding, y + self.padding

        text = self.get_text()
        text.draw(x, y, image, "top")

    @cached_method
    def get_text(self):
        return Text(
            self.textContent,
            self.config,
            self.font,
            self.fontSize
        )


class BarChart(object):
    def __init__(self, min, max, value, unit, fill, outline, config):
        self.min = min
        self.max = max
        self.value = value
        self.unit = unit
        self.fill = fill
        self.outline = outline

        self.padding = 6

        self.barWidth = 4
        self.barHeight = 300
        self.config = config

        self.texts = None

    @cached_method
    def get_size(self):
        width, height = 0, 0

        width += self.barWidth
        width += self.padding

        # Get the maximum width of the texts
        w = 0
        for text in self.get_texts():
            tw, th = text.get_size()
            if w < tw:
                w = tw

        width += w

        height += self.barHeight

        width += 2 * self.padding
        height += 2 * self.padding

        return width, height

    def draw(self, x, y, image):
        w, h = self.get_size()

        background = Rectangle(
            w,
            h,
            self.config["outlineColor"],
            self.config["legendColor"]
        )

        background.draw(x, y, image)

        x, y = x + self.padding, y + self.padding

        bar = Rectangle(
            self.barWidth,
            self.barHeight,
            self.outline
        )

        bar.draw(x, y, image)

        value = Rectangle(
            self.barWidth,
            self.get_value_height(),
            None,
            self.fill
        )

        value.draw(x, y + (self.barHeight / 2), image)

        w, h = bar.get_size()
        x += w + self.padding

        texts = self.get_texts()
        texts[0].draw(x, y, image, valign="top")

        y += self.barHeight / 2
        texts[1].draw(x, y, image, valign="middle")

        y += self.barHeight / 2
        texts[2].draw(x, y, image, valign="bottom")

    @cached_method
    def get_texts(self):
        texts = []

        texts.append(Text(
            u"{} {}".format(self.max, self.unit),
            self.config
        ))

        texts.append(Text(
            u"{} {}".format(self.get_mid(), self.unit),
            self.config
        ))

        texts.append(Text(
            u"{} {}".format(self.min, self.unit),
            self.config
        ))

        return texts

    def get_mid(self):
        return (self.min + self.max) / 2

    def get_value_height(self):
        range = abs(self.min - self.max) / 2
        ratio = (float(self.barHeight) / range) / 2

        valueMidOffset = self.value - self.get_mid()
        valueHeight = int(ratio * valueMidOffset)

        return valueHeight * -1


class Sensors(object):
    def __init__(self, data, config):
        self.data = data
        self.config = config
        self.chartSpacing = 16

    def get_size(self):
        width, height = 0, 0

        for chart in self.get_charts():
            w, h = chart.get_size()

            if height < h:
                height = h

            width += w + self.chartSpacing

        return width, height

    def draw(self, x, y, image):
        for chart in self.get_charts():
            chart.draw(x, y, image)

            w, h = chart.get_size()
            x += w + self.chartSpacing

    @cached_method
    def get_charts(self):
        charts = []

        for index, sensor in enumerate(self.config["sensors"]):
            charts.append(BarChart(
                min(sensor["range"]),
                max(sensor["range"]),
                self.data[index],
                sensor["unit"],
                sensor["color"],
                self.config["outlineColor"],
                self.config
            ))

        return charts


class LegendItem(object):
    def __init__(self, color, text, config):
        self.spacing = 4

        self.text = Text(text, config)

        self.indicatorSize = 16
        self.indicator = Rectangle(
            self.indicatorSize,
            self.indicatorSize,
            config["outlineColor"],
            color
        )

    @cached_method
    def get_size(self):
        width, height = self.text.get_size()

        width += self.spacing
        width += self.indicatorSize

        if height < self.indicatorSize:
            height = self.indicatorSize

        return width, height

    def draw(self, x, y, image):
        self.indicator.draw(x, y, image)
        w, h = self.indicator.get_size()

        x += w + self.spacing

        self.text.draw(x, y + (h / 2), image)


class Legend(object):
    def __init__(self, data, config):
        self.data = data

        self.outline = config["outlineColor"]
        self.fill = config["legendColor"]

        self.config = config

        self.itemSpacing = 32
        self.padding = 6

        self.legendItems = None

    @cached_method
    def get_size(self):
        items = self.get_legend_items()

        width = 0
        height = 0

        for item in items:
            w, h = item.get_size()

            width += w
            if height < h:
                height = h

        width += (len(items) - 1) * self.itemSpacing

        width += 2 * self.padding
        height += 2 * self.padding

        return width, height

    def draw(self, x, y, image):
        width, height = self.get_size()

        background = Rectangle(
            width,
            height,
            self.outline,
            self.fill
        )

        background.draw(x, y, image)

        items = self.get_legend_items()

        x += self.padding
        y += self.padding

        for item in items:
            w, h = item.get_size()

            item.draw(x, y, image)

            x += w + self.itemSpacing

    @cached_method
    def get_legend_items(self):
        legendItems = []

        for index, value in enumerate(self.data):
            sensor = self.config["sensors"][index]
            color = sensor["color"]

            sensorText = u"{} ({:.2f} {})".format(
                sensor["name"],
                float(value),
                sensor["unit"]
            )

            item = LegendItem(
                color,
                sensorText,
                self.config
            )

            legendItems.append(item)

        return legendItems
