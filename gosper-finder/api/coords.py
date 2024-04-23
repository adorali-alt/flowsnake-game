# Coords objects are immutable

import math

class Coords:
    # (x,y,z) coordinates mapped to an isometric triangle grid 
    def __init__(self, x, y, z=0):
        self.x = x       # up right <+-> down left
        self.y = y       # up <+-> down
        self.z = z       # up in <+-> down out

    def getX(self):
        return self.x 

    def getY(self):
        return self.y 

    def getZ(self):
        return self.z

    # TODO consider deleting. things are getting a bit out of scope but this is much better implemented by the matrix handling in app.py while preparing the render
    def get_point(self): 
        cart_y = self.y + (self.x * math.sin(45)) + (self.z * .5)
        return [self.x, cart_y, self.z]

    # Point of interest for understanding directions.
    # Note that up and down is the only cardinal axis we move along. 
    # Due left and due in are not walkable directions. 
    # Instead, those are navigated diagonally in an 'X' pattern. 
    # Comparable to (Eisenstein coords which parse R2 into a hex lattice 
    # as opposed to the square lattice of Cartesian coords). 

    # 2D

    def posIncrUp(self):
        return Coords(self.x, self.y + 1, self.z)

    def posIncrDown(self):
        return Coords(self.x, self.y - 1, self.z)

    def posIncrUpRight(self):
        return Coords(self.x + 1, self.y, self.z)

    def posIncrDownLeft(self):
        return Coords(self.x - 1, self.y, self.z)

    def posIncrUpLeft(self):
        return Coords(self.x - 1, self.y + 1, self.z)

    def posIncrDownRight(self):
        return Coords(self.x + 1, self.y - 1, self.z)

    # 3D expansion

    def posIncrUpIn(self):
        return Coords(self.x, self.y, self.z + 1)

    def posIncrUpOut(self):
        return Coords(self.x, self.y + 1, self.z - 1)

    def posIncrDownIn(self):
        return Coords(self.x, self.y - 1, self.z + 1)

    def posIncrDownOut(self):
        return Coords(self.x, self.y, self.z - 1)

    def posIncrLeftIn(self):
        return Coords(self.x - 1, self.y, self.z + 1)

    def posIncrLeftOut(self):
        return Coords(self.x - 1, self.y + 1, self.z - 1)

    def posIncrRightOut(self):
        return Coords(self.x + 1, self.y, self.z - 1)

    def posIncrRightIn(self):
        return Coords(self.x + 1, self.y - 1, self.z + 1)

    # utils

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<:" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ":>"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, c):
        return c.x == self.x and c.y == self.y and c.z == self.z