class Object:
    """
    Represents a detected object
    """
    # (x, y) is the top left coordinate
    x = None
    y = None
    width = 0
    height = 0
    label = None
    score = .0

    def to_string(self):
        return "x={0}, y={1}\n" \
               "width={2}, height={3}\n" \
               "label='{4}'\n" \
               "score={5}\n"\
            .format(self.x, self.y,
                    self.width, self.height,
                    self.label, self.score)

    def __eq__(self, other):
        return self.x == other.x and \
               self.y == other.y and \
               self.width == other.width and \
               self.height == other.height and \
               self.label == other.label and \
               self.score == other.score