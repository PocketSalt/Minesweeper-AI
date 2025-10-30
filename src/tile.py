class Tile:
    # static flag count
    correctFlagCount = 0

    # constructor with value, and visibility
    def __init__(self, val: int, vis: bool):
        self.value = val
        self.visible = vis
        self.flagged = False

    # reveal self.
    def reveal(self):
        self.visible = True

    # flag on/off
    def flag(self):
        self.flagged = not self.flagged

        # if bomb, ++ flag count
        if self.value == -1:
            Tile.correctFlagCount += 1 if self.flagged else -1

    def getValue(self):
        if self.visible and not self.flagged:
            return self.value
        else:
            return -2