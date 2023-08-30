# Coords objects are immutable

class Coords:

    # (x,y,z) coordinates mapped to an isometric hex grid, with x = /, y = |, z = \
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def posIncrN(self):
    	return Coords(self.x, self.y + 1, self.z)

    def posIncrNE(self):
    	return Coords(self.x + 1, self.y, self.z)

    def posIncrNE(self):
    	return Coords(self.x, self.y, self.z - 1)

    def posIncrS(self):
    	return Coords(self.x, self.y - 1, self.z)

    def posIncrSW(self):
    	return Coords(self.x - 1, self.y, self.z)

    def posIncrW(self):
    	return Coords(self.x - 1, self.y self.z + 1)

    def posIncrE(self):
    	return Coords(self.x + 1, self.y, self.z - 1)

    def posIncrNW(self):
    	return Coords(self.x, self.y, self.z + 1)

    def __eq__(self, c):
        return isinstance(obj, c) and c.x == self.x && c.y == self.y && c.z == self.z
