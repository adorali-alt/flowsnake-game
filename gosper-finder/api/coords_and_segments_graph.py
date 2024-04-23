import coords
from line import *
import triangular_plane
import tetrahedral_disphenoid

# graph class knows about the adjacency of generator flags. 
# its vertices are corners that 1-3 generator flags may touch.
# and its edges are generator flag segments.

class CoordsAndSegmentsGraph:

    # GETTERS

    def get_start_corner(self):
        return self.start_corner_coords

    # l :: list of Coords 
    # o :: origin coord
    # Returns sorted [], all segments touching this coord which are "in play" AKA available to be selected.
    def get_in_play_adjacent_segments_list(self, l):
        result = []
        for c in l:
            segments = self.adjDict[c]
            for s in segments:
                if s.is_in_play == True:
                    result.append(s)
        return sorted(result)

    # c :: Coords 
    # Returns sorted [], all segments touching this coord which are "in play" AKA available to be selected.
    # Note: sorted because manager's autosolve needs to avoid pre-explored paths. see autosolve
    def get_in_play_adjacent_segments(self, c):
        result = []
        segments = self.adjDict[c]
        for s in segments:
            if s.is_in_play == True:
                result.append(s)
        return sorted(result)

    def get_adjacent_segments(self, c):
        return self.adjDict[c]

    def get_all_segments(self):
        return self.segments_to_flag_lookup_table.keys()

    def get_all_flags(self):
        return self.flag_set

    def get_all_coords(self):
        return self.adjDict.keys()

    def get_magic_coords(self):
        return self.magic_coords

    def get_flag_from_segment(self, segment):
        if segment in self.segments_to_flag_lookup_table:
            return self.segments_to_flag_lookup_table[segment].segments_array
        else:
            print("error get_flag_from_segment : " + str(segment) + " not in lookup table")
            return None


    # SETTERS


    # Handles "choosing" and "unchoosing" a segment. Also handles that action's ramifications for 
    # the other segments with which it shares a flag.
    def set_flag_in_play(self, segment, b):
        for s in self.segments_to_flag_lookup_table[segment].segments_array:
            s.set_in_play(b)

    def set_segment_in_play(self, s, b):
        s.set_in_play(b)


    # SETUP FUNCTIONS


    # Returns int, unique numeric id 
    # don't think about int overflows ( honestly generators won't get that big )
    def generate_id(self):
        self.curr_id += 1
        return self.curr_id - 1

    # c :: Coords, left corner of the flag to have its segments spawned (in 2D looks like '<|')
    # Returns GeneratorFlag 
    # Useful for building the 2D generator because all flags are pointed the same way
    def spawn_flag_2D(self, c):
        return self.spawn_flag_3D(c.posIncrUpRight(), c, c.posIncrDownRight())

    # c :: Coords, left corner of the flag to have its segments spawned (in 2D looks like '<|')
    # Returns GeneratorFlag 
    def spawn_flag_3D(self, c1, c2, c3):
        return triangular_plane.Tri(c2,
            [Line(self.generate_id(), Direction.SW, c1, c2),
            Line(self.generate_id(), Direction.SE, c2, c3),
            Line(self.generate_id(), Direction.N, c3, c1)],
            self.generate_id())

    # c :: Coords, top corner of the pyramid to have its triangles spawned.
    # Returns GeneratorFlag 
    # Not like in 2D, will spawn BOTH flags associated with this pyramid's octahedron not just one. 
    # left inner then right outer
    def spawn_flag_in(self, c):
        # t, s, b
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c, c.posIncrUpIn(), c.posIncrLeftIn()), 
                    self.spawn_flag_3D(c.posIncrUpIn(), c, c.posIncrDownIn()), 
                    self.spawn_flag_3D(c.posIncrLeftIn(), c, c.posIncrDownIn()),
                    self.spawn_flag_3D(c.posIncrUpIn(), c.posIncrLeftIn(), c.posIncrDownIn())]))
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c.posIncrUpIn().posIncrDownIn(), c.posIncrUpIn(), c.posIncrRightIn()),
                    self.spawn_flag_3D(c.posIncrDownIn(), c.posIncrRightIn(), c.posIncrUpIn()),
                    self.spawn_flag_3D(c.posIncrUpIn(), c.posIncrUpIn().posIncrDownIn(), c.posIncrDownIn()),
                    self.spawn_flag_3D(c.posIncrRightIn(), c.posIncrDownIn(), c.posIncrUpIn().posIncrDownIn())]))

    def spawn_flag_uro(self, c):
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c, c.posIncrUpOut(), c.posIncrUp()), 
                    self.spawn_flag_3D(c.posIncrUp(), c.posIncrUpRight(), c),
                    self.spawn_flag_3D(c.posIncrUpRight(), c.posIncrUp(), c.posIncrUpOut()),
                    self.spawn_flag_3D(c.posIncrUpOut(), c, c.posIncrUpRight())]))
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c.posIncrUpOut(), c.posIncrUpOut().posIncrUpRight(), c.posIncrUpRight()),
                    self.spawn_flag_3D(c.posIncrUpRight(), c.posIncrUpOut().posIncrDownRight(), c.posIncrUpOut()),
                    self.spawn_flag_3D(c.posIncrUpOut().posIncrDownRight(), c.posIncrUpRight(), c.posIncrUpOut().posIncrUpRight()),
                    self.spawn_flag_3D(c.posIncrUpOut().posIncrUpRight(), c.posIncrUpOut(), c.posIncrUpOut().posIncrDownRight())]))

    def spawn_flag_dlo(self, c):
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c.posIncrLeftOut(), c.posIncrDownOut(), c), 
                    self.spawn_flag_3D(c, c.posIncrDownLeft(), c.posIncrLeftOut()),
                    self.spawn_flag_3D(c.posIncrDownLeft(), c, c.posIncrDownOut()),
                    self.spawn_flag_3D(c.posIncrDownLeft(), c.posIncrLeftOut(), c.posIncrDownOut())]))
        self.add_generator_flag(tetrahedral_disphenoid.Tetra(
                    [self.spawn_flag_3D(c.posIncrDownLeft(), c.posIncrDownLeft().posIncrDownOut(), c.posIncrDownOut()),
                    self.spawn_flag_3D(c.posIncrDownOut(), c.posIncrDown(), c.posIncrDownLeft()),
                    self.spawn_flag_3D(c.posIncrDown(), c.posIncrDownOut(), c.posIncrDownOut().posIncrDownLeft()),
                    self.spawn_flag_3D(c.posIncrDown(), c.posIncrDownLeft(), c.posIncrDownLeft().posIncrDownOut())]))

    # flag :: GeneratorFlag
    def add_generator_flag(self, flag):
        for segment in flag.get_segments_array():
            for c in segment.get_all_coords():
                if c not in self.adjDict:
                    self.adjDict[c] = set()
                self.adjDict[c].add(segment)

            self.segments_to_flag_lookup_table[segment] = flag
        self.flag_set.add(flag)


    def form_hexagon(self, n, curr):
        # initial row
        unsaturated_coords = []
        self.magic_coords = set()

        flag = self.spawn_flag_2D(curr)
        self.add_generator_flag(flag)
        unsaturated_coords.append(flag.get_top_coords())
        unsaturated_coords.append(flag.get_bottom_coords())
        curr = curr.posIncrDown()
        for x in range(n - 1):
            flag = self.spawn_flag_2D(curr)
            self.add_generator_flag(flag)
            unsaturated_coords.append(flag.get_bottom_coords())
            curr = curr.posIncrDown()

        # form ascending rows
        for x in range(n - 1):
            unsaturated_coords = self.form_hexagon_helper(unsaturated_coords)

        self.magic_coords.add(unsaturated_coords[len(unsaturated_coords) - 1])

        # form descending rows
        for x in range(n - 1):
            # pruning
            unsaturated_coords.pop(0)
            unsaturated_coords.pop()
            unsaturated_coords = self.form_hexagon_helper(unsaturated_coords)

        self.magic_coords.add(unsaturated_coords[len(unsaturated_coords) - (n + 1)])
            

    def form_hexagon_helper(self, unsaturated_coords):
        new_unsaturated_coords = []
        flag = self.spawn_flag_2D(unsaturated_coords.pop(0))
        self.add_generator_flag(flag)
        new_unsaturated_coords.append(flag.get_top_coords())
        new_unsaturated_coords.append(flag.get_bottom_coords())
        for c in unsaturated_coords:
            flag = self.spawn_flag_2D(c)
            self.add_generator_flag(flag)
            new_unsaturated_coords.append(flag.get_bottom_coords())
        return new_unsaturated_coords


    # it looks a lot like a starbit from mario galaxy but more precisely we're 
    # building a stellated rhombic dodecahedron. 
    # see https://en.wikipedia.org/wiki/Stars_(M._C._Escher) for a 
    # solid (lower right) or skeletonized (center) depiction
    def form_starbit(self):
        distant_left = coords.Coords(-1, -2, 3)     # farthest left down point
        distant_right = coords.Coords(1, -1, 3)     # farthest right top point 
        orbit = coords.Coords(0, 0, 0)              # closest point
        self.magic_coords = [orbit, distant_right, distant_left]

        # place an octahedron in every direction 
        self.spawn_flag_in(orbit)
        self.spawn_flag_in(orbit.posIncrRightIn())
        self.spawn_flag_in(orbit.posIncrLeftIn())
        self.spawn_flag_in(orbit.posIncrRightIn().posIncrLeftIn())

        self.spawn_flag_uro(distant_left)
        self.spawn_flag_uro(distant_left.posIncrUp())
        self.spawn_flag_uro(distant_left.posIncrRightOut())
        self.spawn_flag_uro(distant_left.posIncrRightOut().posIncrUp())

        self.spawn_flag_dlo(distant_right)
        self.spawn_flag_dlo(distant_right.posIncrLeftOut())
        self.spawn_flag_dlo(distant_right.posIncrDown())
        self.spawn_flag_dlo(distant_right.posIncrDown().posIncrLeftOut())


    # initial_row_size :: int, num of flags on one edge of the generator
    def __init__(self, initial_row_size, generate_3D=False):
        self.curr_id = 0                        # counter for segments unique ids
        self.adjDict = {}                       # coords -> adjacent segments
        self.flag_set = set()
        self.segments_to_flag_lookup_table = {} # correlates each seg to its flag

        self.start_corner_coords = coords.Coords(0, 0)
        if generate_3D:
            self.form_starbit()
        else:
            self.form_hexagon(initial_row_size, self.start_corner_coords)
            
        
