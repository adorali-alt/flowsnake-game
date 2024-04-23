class Tetra():

    def __init__(self, segments_array):
        self.segments_array = segments_array # '<|' :: [front, back, top, bottom]

    def get_segments_array(self):
        return self.segments_array

    def get_all_coords(self):
        all_coords = []
        for s in self.segments_array:
            all_coords.append(s.get_all_coords())
        return all_coords

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{:" + str(self.get_all_coords())+ ":}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, f):
        # consider speeding up by not rearraying all coords or try using hash
        is_same = True
        for s in self.get_all_coords():
            is_same = is_same and s in f.get_all_coords()
        return is_same