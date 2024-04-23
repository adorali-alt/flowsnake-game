import os, sys

sys.path.insert(1, os.getcwd()) 

import unittest
import coords
from segment import *
import coords_and_segments_graph
import game_state_manager


class TestGraph(unittest.TestCase):

    def test_init(self):
        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2)
        self.assertEqual(len(generator_flag_graph.get_all_flags()), 7, "Should be 7")
        self.assertEqual(len(generator_flag_graph.get_all_segments()), 7 * 3, "Should be 21")
        self.assertEqual(len(generator_flag_graph.get_all_coords()), 12, "Should be 12")

        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(3)
        self.assertEqual(len(generator_flag_graph.get_all_flags()), 19, "Should be 19")
        self.assertEqual(len(generator_flag_graph.get_all_segments()), 19 * 3, "Should be 21")
        self.assertEqual(len(generator_flag_graph.get_all_coords()), 27, "Should be 27")

        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(4)
        self.assertEqual(len(generator_flag_graph.get_all_flags()), 37, "Should be 19")
        self.assertEqual(len(generator_flag_graph.get_all_segments()), 37 * 3, "Should be 21")
        self.assertEqual(len(generator_flag_graph.get_all_coords()), 48, "Should be 48")

        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2, True)
        self.assertEqual(len(generator_flag_graph.get_all_flags()), 28, "Should be 28")
        self.assertEqual(len(generator_flag_graph.get_all_segments()), 28 * 3, "Should be 28 * 3")

    def test_set_flag_in_play(self):
        initial_row_size = 2
        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(initial_row_size)

        # mimics the case of starting at 0, 0 and choosing seg ending at 1, -1
        segment = generator_flag_graph.get_in_play_adjacent_segments(coords.Coords(1, -1))[0]
        generator_flag_graph.set_flag_in_play(segment, False)

        # flag attached to the chosen segment should be out of play
        segments_arr = generator_flag_graph.get_flag_from_segment(segment)
        self.assertEqual(len(segments_arr), 3)
        for s in segments_arr:
            self.assertFalse(s.get_is_in_play(), "segment still in play")

        # every other flag should still be returned
        expected_segments = ([ 
            [coords.Coords(1, -1), coords.Coords(0, -1)], [coords.Coords(1, -2), coords.Coords(1, -1)], 
            [coords.Coords(2, -1), coords.Coords(1, -1)], [coords.Coords(1, -1), coords.Coords(2, -2)]])
        actual = generator_flag_graph.get_in_play_adjacent_segments(coords.Coords(1, -1))

        self.segment_endpoint_checker(expected_segments, actual)


    def test_get_in_play_adjacent_segments(self):
        initial_row_size = 2
        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(initial_row_size)

        # corner case
        expected_segments = [[coords.Coords(1, 0), coords.Coords(0, 0)], [coords.Coords(0, 0), coords.Coords(1, -1)]]
        segments = generator_flag_graph.get_in_play_adjacent_segments(coords.Coords(0, 0))
        self.segment_endpoint_checker(expected_segments, segments)

        # middle case
        expected_segments = ([[coords.Coords(0, 0), coords.Coords(1, -1)], [coords.Coords(1, -1), coords.Coords(1, 0)], 
            [coords.Coords(1, -1), coords.Coords(0, -1)], [coords.Coords(1, -2), coords.Coords(1, -1)], 
            [coords.Coords(2, -1), coords.Coords(1, -1)], [coords.Coords(1, -1), coords.Coords(2, -2)]])
        segments = generator_flag_graph.get_in_play_adjacent_segments(coords.Coords(1, -1))
        self.segment_endpoint_checker(expected_segments, segments)


    def segment_endpoint_checker(self, expected, actual):
        self.assertEqual(len(expected), len(actual), "mismatched lengths")
        i = 0
        while i < len(actual):
            self.assertEqual(expected[i][0], actual[i].get_coords_former(), "mismatched value")
            self.assertEqual(expected[i][1], actual[i].get_coords_later(), "mismatched value")
            i+=1

    def test_is_end(self):
        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(2)
        i = 0
        print(2)
        for s in generator_flag_graph.get_all_segments():
            if s.is_end(generator_flag_graph.get_magic_coords()):
                print(s)
                i+=1
        self.assertEqual(i, 4)

        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(3)
        i = 0
        print(3)
        for s in generator_flag_graph.get_all_segments():
            if s.is_end(generator_flag_graph.get_magic_coords()):
                print(s)
                i+=1
        self.assertEqual(i, 4)

        generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(4)
        i = 0
        print(4)
        for s in generator_flag_graph.get_all_segments():
            if s.is_end(generator_flag_graph.get_magic_coords()):
                print(s)
                i+=1
        self.assertEqual(i, 4)


    def test_build_l_system(self):
        # hardcode a legal solution for size 2
        solution_stack_a = []
        c = coords.Coords(0, 0)
        solution_stack_a.append(Segment(0, Direction.N, c, c.posIncrDown()))
        c = c.posIncrDown()
        solution_stack_a.append(Segment(1, Direction.SE, c.posIncrDownRight(), c))
        c = c.posIncrDownRight()
        solution_stack_a.append(Segment(2, Direction.N, c.posIncrUp(), c))
        c = c.posIncrUp()
        solution_stack_a.append(Segment(3, Direction.SW, c, c.posIncrUpRight()))
        c = c.posIncrUpRight()
        solution_stack_a.append(Segment(4, Direction.N, c, c.posIncrDown()))
        c = c.posIncrDown()
        solution_stack_a.append(Segment(5, Direction.N, c, c.posIncrDown()))
        c = c.posIncrDown()
        solution_stack_a.append(Segment(6, Direction.SW, c.posIncrDownLeft(), c))

        manager = game_state_manager.GameStateManager(2)
        manager.set_selected_path_stack(solution_stack_a)
        manager.produce_l_system()


    # AAA+BBB+AA+BBB+A+BB+A+B++B-A--AA-B-AA-BB-AAA-BB-AAAA-BBB+
    # -AAA+BBBB+AA+BBB+AA+BB+A+BB++B+A--A-B-AA-B-AAA-BB-AAA-BBB
    # ^ 2D size 4 solution (~ 2203.028s)

    def test_auto_solve(self):
        manager = game_state_manager.GameStateManager(2)
        manager.auto_solve()


if __name__ == '__main__':
    unittest.main()

# RUN WITH python test_graph_unittest.py
# see https://docs.python.org/3/library/unittest.html
