import coords
from enum import IntEnum

# \ / or | 
# For 2D triangular flags, this enum cycles counterclockwise.
# 
# Rule source: https://www.researchgate.net/publication/236966236_New_Gosper_Space_Filling_Curves, page 2, rule P9
class Direction(IntEnum):
    SW = 1
    SE = 2
    N = 3

    def succ(self):
        v = self.value + 1
        if v > 3:
            v = 1
        return Direction(v)

    def pred(self):
        v = self.value - 2
        if v < 1:
            v = 3
        return Direction(v)

class Line():

    # unique_id :: int
    # line_type :: Direction
    # coords_former :: Coords, the more clockwise side of this line
    # coords_later :: Coords, the more counterclockwise side of this segment 
    def __init__(self, unique_id, line_type, coords_former, coords_later):
        self.unique_id = unique_id 
        self.coords_former = coords_former
        self.coords_later = coords_later
        self.line_type = line_type 
        self.is_in_play = True

    # prev :: the last segment in path prior to *self*
    # rule_a :: string 
    # rule_b :: string 
    # flow_direction :: boolean, acts as cyclical enum for choosing 
    #                       btwn recursion type A or B
    def build_l_system(self, prev, rule_a, rule_b, flow_direction):
        flows_with = self.flows_with(prev, self.shared_coord(prev))

        # handle turns
        if prev.line_type.succ().value == self.line_type.value:
            if flows_with: 
                rule_a.append("-")
                rule_b.insert(0, "+")
                rule_a.append("-") 
                rule_b.insert(0, "+")
            else:
                rule_a.append("+") 
                rule_b.insert(0, "-")

        elif prev.line_type.succ().succ().value == self.line_type.value:
            if flows_with: 
                rule_a.append("+") 
                rule_b.insert(0, "-")
                rule_a.append("+") 
                rule_b.insert(0, "-")
            else:
                rule_a.append("-") 
                rule_b.insert(0, "+")

        # decide A type recursive segment or B type
        if flows_with is False:
            flow_direction = not flow_direction

        if flow_direction is True:
            rule_a.append("A") 
            rule_b.insert(0, "B")
        else:
            rule_a.append("B") 
            rule_b.insert(0, "A")

        return flow_direction
        


    # SETTERS

    def set_in_play(self, b):
        self.is_in_play = b

    # GETTERS

    def get_unique_id(self):
        return self.unique_id

    def line_type(self):
        return self.line_type

    def get_coords_later(self):
        return self.coords_later

    def get_coords_former(self):
        return self.coords_former

    def is_in_play(self):
        return self.is_in_play

    def get_all_coords_renderable(self):
        return [self.coords_former.get_point(), self.coords_later.get_point()]

    def get_all_coords(self):
        return [self.coords_former, self.coords_later]

    def to_vector(self):
        return [self.coords_later.getX() - self.coords_former.getX(), self.coords_later.getY() - self.coords_former.getY(), self.coords_later.getZ() - self.coords_former.getZ()]


    # UTILS 

    def step_across(self, c):
        if c == self.coords_later:
            return self.coords_former
        elif c == self.coords_former:
            return self.coords_later
        else:
            print("error :: step_across coords don't match. c=" + str(c)) 
            print("  coords_later=" + str(self.coords_later))
            print("  coords_former=" + str(self.coords_former))

    # Given adjacent line from another triangle, and the shared coord, returns True if the lines "flow with" 
    # and False if the lines "flow against" each other. 
    # refer to Direction enum 
    def flows_with(self, prev, shared_coord):
        return (self.get_coords_former() == shared_coord and prev.get_coords_later() == shared_coord or 
            prev.get_coords_former() == shared_coord and self.get_coords_later() == shared_coord) 

    # Returns true if this line is a legal path terminator and false otherwise. 
    def is_end(self, magic_coords):
        return self.coords_later in magic_coords or self.coords_former in magic_coords

    def shared_coord(self, o):
        o_coords = [o.get_coords_former(), o.get_coords_later()]
        if self.get_coords_former() in o_coords:
            return self.get_coords_former()
        elif self.get_coords_later() in o_coords:
            return self.get_coords_later()
        else:
            print("!! no shared coords")
            print(o)
            print(self)
            return None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "-:" + str(self.unique_id) + ", " + str(self.get_coords_former()) + ", " + str(self.get_coords_later()) + ":-"

    def __hash__(self):
        return hash(str(self.get_coords_former()) + ", " + str(self.get_coords_later()))

    def __eq__(self, s):
        return s.get_coords_former() == self.get_coords_former() and s.get_coords_later() == self.get_coords_later()

    # note: From a purely logical point of view, the segment objects can't 
    # really be greater than or lesser than each other, but they need to be 
    # placed in a stable sorted order to speed up the game 
    # manager's autosolve functionality. unique_id is a good choice because 
    # it's fast to compare, unique, and will never change.

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __le__(self, other):
        return self.unique_id <= other.unique_id

    def __gt__(self, other):
        return self.unique_id > other.unique_id

    def __ge__(self, other):
        return self.unique_id >= other.unique_id
