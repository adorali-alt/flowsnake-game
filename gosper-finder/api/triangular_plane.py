
class Tri():

    def __init__(self, side_coords, segments_array, unique_id=0):
        # the coords of the side corner of the flag. other corner locations are inferred
        self.side_coords = side_coords 
        self.bottom_coords = segments_array[2].get_coords_former()
        self.top_coords = segments_array[2].get_coords_later()
        self.segments_array = segments_array # sw, se, n
        self.is_in_play = True 
        self.unique_id = unique_id # unique_id default value used when tris aren't segments

    def is_end(self, magic_coords):
        return (self.side_coords in magic_coords or 
            self.bottom_coords in magic_coords or 
            self.top_coords in magic_coords)

    def get_all_coords(self):
        return [self.side_coords, self.bottom_coords, self.top_coords]

    def get_all_coords_hex(self):
        return [[self.side_coords.getX(), self.side_coords.getY(), self.side_coords.getZ()], 
        [self.bottom_coords.getX(), self.bottom_coords.getY(), self.bottom_coords.getZ()], 
        [self.top_coords.getX(), self.top_coords.getY(), self.top_coords.getZ()]]

    # helps with planar math when getting ready for 3D rendering
    # returns a list of two vectors representing two sides of the plane
    def get_two_vectors(self):
        lst1 = [self.side_coords.getX() - self.bottom_coords.getX(), 
                    self.side_coords.getY() - self.bottom_coords.getY(),
                    self.side_coords.getZ() - self.bottom_coords.getZ()]
        lst2 = [self.side_coords.getX() - self.top_coords.getX(), 
                    self.side_coords.getY() - self.top_coords.getY(),
                    self.side_coords.getZ() - self.top_coords.getZ()]
        return [lst1, lst2]

    def get_all_coords_renderable(self):
        return [self.side_coords.get_point(), self.bottom_coords.get_point(), self.top_coords.get_point()]

    def set_in_play(self, b):
        self.is_in_play = b

    def step_across(self, c):
        r = self.get_all_coords()
        r.remove(c)
        return r

    def shared_coord(self, o):
        for c in o.get_all_coords():
            if c in self.get_all_coords():
                return c
        print("error :: shared_coord " + str(self)+ " and " + str(o) + " no shared coord")

    def get_side_coords(self):
        return self.side_coords

    def get_bottom_coords(self):
        return self.bottom_coords

    def get_top_coords(self):
        return self.top_coords

    def get_segments_array(self):
        return self.segments_array

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{:" + str(self.get_all_coords())+ ":}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, f):
        return (self.side_coords in f.get_all_coords() and 
            self.top_coords in f.get_all_coords() and 
            self.bottom_coords in f.get_all_coords())

    # note: From a purely logical point of view, the segment objects can't 
    # really be greater than or lesser than each other, but they need to be 
    # placed in a stable sorted order to speed up the game 
    # manager's autosolve functionality. unique_id is a good choice because 
    # it's fast to compare, unique, and will never change. see also compares in line.py

    def __lt__(self, other):
        return self.unique_id < other.unique_id

    def __le__(self, other):
        return self.unique_id <= other.unique_id

    def __gt__(self, other):
        return self.unique_id > other.unique_id

    def __ge__(self, other):
        return self.unique_id >= other.unique_id
