from PIL import Image, ImageEnhance

class Filter:

    __slots__ = ["name",
                 "contrast",
                 "brightness",
                 "saturation",
                 "color_temperature_change",
                 "color_thresholds"]

    def __init__(self,
                 name,
                 contrast: float = 1.0,
                 brightness: float = 1.0,
                 saturation: float = 1.0,
                 color_temperature_change: int = 0,
                 color_thresholds: tuple = (0, 0, 0, 0)):  # RGBW

        self.name = name
        self.contrast = contrast
        self.brightness = brightness
        self.saturation = saturation
        self.color_temperature_change = color_temperature_change
        self.color_thresholds = color_thresholds

    def apply_config(self, image_path, preview=True):

        self.set_current_preset()
        image = Image.open(image_path)

        def adjust_contrast(image):
            im_contrast = ImageEnhance.Contrast(image)
            return im_contrast.enhance(self.contrast)

        def adjust_brightness(image):
            im = ImageEnhance.Brightness(image)
            return im.enhance(self.brightness)

        def adjust_saturation(image):
            im = ImageEnhance.Color(image)
            return im.enhance(self.saturation)

        def apply_threshold(image):

            if (thresh := self.color_thresholds[3]):
                return image.convert("L").point((lambda x: 255 if x > thresh else 0), mode="1")

            rgb_channels = []

            for channel, threshold in zip(image.split(), self.color_thresholds[0:3]):
                rgb_channels.append(channel.point(lambda x: 255 if x > threshold else 0))

            return Image.merge("RGB", rgb_channels)

        def adjust_color_temperature(image, r_change=20, b_change=-20):

            r, _, b = image.split()

            r_channel = r.point(lambda x: (x + self.color_temperature_change * r_change))
            b_channel = b.point(lambda x: (x + self.color_temperature_change * b_change))

            return Image.merge("RGB", (r_channel, _, b_channel))

        if self.contrast != float(1.0):
            image = adjust_contrast(image)
            #image.show()

        if self.brightness != float(1.0):
            image = adjust_brightness(image)
            #image.show()

        if self.saturation != float(1.0):
            image = adjust_saturation(image)
            #image.show()

        if self.color_temperature_change != 0:
            image = adjust_color_temperature(image)
            #image.show()

        if any(self.color_thresholds) is True:
            image = apply_threshold(image)
            #image.show()

        if preview:
            image.show()
        else:
            image.save(image_path)

    def set_current_preset(self):
        Filter_Presets.current_filter = self

    def __str__(self):
        return str(self.name)

class Filter_Presets:

    filter_dict = {
        "Original": Filter("Original"),
        "Grau": Filter("Grau", saturation=0.0),
        "Schwarzweiß": Filter("Schwarzweiß", brightness=1.2, color_thresholds=(0, 0, 0, 175)),
        "Warm": Filter("Warm", color_temperature_change=+2),
        "Kalt": Filter("Kalt", color_temperature_change=-2),
        "Poster": Filter("Poster", brightness=1.0, contrast=1.2, color_thresholds=(170, 170, 170, 0))
        }

    current_filter = filter_dict["Original"]