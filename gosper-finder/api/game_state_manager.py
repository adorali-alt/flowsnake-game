import coords_and_segments_graph
import math
from line import *
from bisect import bisect_left
from collections import deque


class GameStateManager:


	# SETUP FUNCTIONS

	def __init__(self, initial_row_size, generate_3D=False):
		# Holds all selected flags in order
		self.initial_row_size = initial_row_size
		self.selected_path_stack = deque()
		# Handles flags wrt each other. For example, quickly finds adjacent flags.
		self.generator_flag_graph = coords_and_segments_graph.CoordsAndSegmentsGraph(initial_row_size, generate_3D)
		self.start_corner_coords = self.generator_flag_graph.get_start_corner()
		self.curr_corner_coords = self.start_corner_coords
		# [] of next segment options
		self.valid_next_options = self.load_valid_next_options(self.curr_corner_coords)
		self.l_system = None
		self.generate_3D = generate_3D

	# GETTERS 

	def get_start_segments(self):
		nexts = []
		for segment in self.generator_flag_graph.get_in_play_adjacent_segments(self.generator_flag_graph.get_start_corner()):
			nexts.append(segment.get_unique_id())
		return nexts

	def get_all_flags_renderable(self):
		return self.all_flags_renderable

	def get_selected_path_ids(self):
		return self.selected_path_ids

	def get_selected_path_stack(self):
		return self.selected_path_stack

	# Returns [], the newest valid choosable segments given the Coords c
	def load_valid_next_options(self, c):
		return self.generator_flag_graph.get_in_play_adjacent_segments(c)



	# SOLVE LOGIC


	# This algorithm defines a continuous path from start_coords to an acceptable end_coord made up of segments 
	# where every flag contributes exactly one segment.
	def auto_solve(self):
		# curr_coords = self.start_corner_coords 
		# segment = None

		path_not_found = True
		surpressed_segments = set()
		invalidating_coords_to_segments = {} 		
		# ^ invalidating_coords_to_segments :: a segment becomes unchoosable if its being chosen would create a branch on the existing path. 
		#                Handling that case, invalidating_coords key is the coord that must be "unchosen" before value [segments]
		#                is viable again.
		last_known_coord = deque() # facillitates unwinding bad solutions, essentially a curr stack
		last_known_coord.append(self.start_corner_coords)
		possible_forward_coords = [self.start_corner_coords]

		while path_not_found is True:

			next_options = self.generator_flag_graph.get_in_play_adjacent_segments_list(possible_forward_coords) 
			# if (len(self.selected_path_stack) > 0):
			# 	next_options = [item for item in next_options if self.filter_helper(item, last_known_coord[-1])]  
			next_options = [item for item in next_options if item not in surpressed_segments]   # branch prevention filter
			prev_segment = None
		
			if len(next_options) == 0:
				
				# bad ending- unchoose until we find the next viable segment
				prev_segment = self.selected_path_stack.pop()
				prev_curr = last_known_coord.pop()

				self.handle_segment_unchoosing(invalidating_coords_to_segments, surpressed_segments, prev_segment.get_all_coords(), prev_segment)
				self.generator_flag_graph.get_in_play_adjacent_segments(prev_curr)

				next_options = self.generator_flag_graph.get_in_play_adjacent_segments(prev_curr)
				# if (len(self.selected_path_stack) > 0):
				# 	next_options = [item for item in next_options if self.filter_helper(item, last_known_coord[-1])]  
				next_options = [item for item in next_options if item not in surpressed_segments]
 
				while self.find_next(next_options, prev_segment) is None and len(self.selected_path_stack) > 0:
					prev_segment = self.selected_path_stack.pop()
					if len(last_known_coord) == 0:
						prev_curr = self.start_corner_coords
					else:
						prev_curr = last_known_coord.pop()
					self.handle_segment_unchoosing(invalidating_coords_to_segments, surpressed_segments, prev_segment.get_all_coords(), prev_segment) 

					next_options = self.generator_flag_graph.get_in_play_adjacent_segments(prev_curr)
					# if (len(self.selected_path_stack) > 0):
					# 	next_options = [item for item in next_options if self.filter_helper(item, last_known_coord[-1])]  
					next_options = [item for item in next_options if item not in surpressed_segments]
					

			# choose segment

			segment = self.find_next(next_options, prev_segment)

			possible_branch_coords = []
			# inital case: start from start lol
			if len(last_known_coord) == 0:
				last_known_coord.append(self.start_corner_coords)

			# midway case: add the coord that's "in-path", not out to the side
			if len(self.selected_path_stack) > 0:
				last_known_coord.append(self.selected_path_stack[-1].shared_coord(segment))
				possible_branch_coords.append(self.selected_path_stack[-1].shared_coord(segment))

			possible_branch_coords.append(last_known_coord[-1])
			possible_forward_coords = segment.get_all_coords()
			possible_forward_coords.remove(last_known_coord[-1]) 

			self.selected_path_stack.append(segment)
			self.handle_segment_choosing(invalidating_coords_to_segments, surpressed_segments, possible_branch_coords, segment) 

			if len(self.selected_path_stack) == len(self.generator_flag_graph.get_all_flags()): 
				# print("trying to end")
				if self.generate_3D:
					path_not_found = (not self.selected_path_stack[len(self.selected_path_stack) - 1].is_end_3D() or 
						(last_known_coord[-1] in invalidating_coords_to_segments and len(invalidating_coords_to_segments[last_known_coord[-1]]) > 0))
				else:
					path_not_found = not self.selected_path_stack[len(self.selected_path_stack) - 1].is_end(self.generator_flag_graph.get_magic_coords())

		print(self.selected_path_stack)
		self.produce_l_system()
		print("done")

	
	def filter_helper(self, item, last_known_coord):
		# set(self.selected_path_stack[-1].get_all_coords().remove(last_known_coord[-1])).issuperset(item.get_all_coords())
		# a bit of a mess
		l = self.selected_path_stack[-1].get_all_coords()
		l.remove(last_known_coord)
		set(l).issuperset(item.get_all_coords())

	def handle_segment_unchoosing(self, invalidating_coords_to_segments, surpressed_segments, possible_branch_coords, s):
		# handle flag
		self.generator_flag_graph.set_flag_in_play(s, True)        

		# handle segments surpressed by this coord having been previously in-path
		for c in possible_branch_coords:
			if c in invalidating_coords_to_segments:
				for segment in invalidating_coords_to_segments[c]:
					surpressed_segments.remove(segment)
				invalidating_coords_to_segments[c] = []

	def handle_segment_choosing(self, invalidating_coords_to_segments, surpressed_segments, possible_branch_coords, s):
		# handle flag
		self.generator_flag_graph.set_flag_in_play(s, False)  

		# handle newly surpressed coords 
		for c in possible_branch_coords:
			if c not in invalidating_coords_to_segments:   
				invalidating_coords_to_segments[c] = []
		
			segments_touching_curr = self.generator_flag_graph.get_adjacent_segments(c)
			for segment in (set(segments_touching_curr) - surpressed_segments):
				invalidating_coords_to_segments[c].append(segment)
				surpressed_segments.add(segment)        


	# best solution so far. only starbit, no inner flags
# 	...deque([-:7, <:0, 0, 1:>, <:0, 0, 0:>:-, -:0, <:0, 0, 2:>, <:0, 0, 1:>:-, -:20, <:1, -1, 3:>, <:0, 0, 2:>:-, -:43, <:0, -1, 3:>, <:1, -1, 3:>:-, -:37, <:0, -1, 3:>, <:-1, 0, 3:>:-, -:59, <:-1, 0, 3:>, <:-1, -1, 3:>:-, -:41, <:0, -2, 4:>, <:-1, -1, 3:>:-, -:47, <:0, -2, 4:>, <:1, -2, 3:>:-, -:32, <:1, -3, 3:>, <:1, -2, 3:>:-, -:52, <:0, -2, 3:>, <:1, -3, 3:>:-, -:49, <:0, -2, 3:>, <:-1, -2, 3:>:-, -:71, <:-1, -2, 3:>, <:0, -2, 2:>:-, -:17, <:-1, -1, 1:>, <:0, -2, 2:>:-, -:64, <:-1, -1, 2:>, <:-1, -1, 1:>:-, -:67, <:-1, -1, 2:>, <:-2, 0, 2:>:-, -:61, <:-1, 0, 2:>, <:-2, 0, 2:>:-, -:55, <:-1, 0, 2:>, <:-1, 1, 1:>:-, -:5, <:-1, 1, 1:>, <:-1, 0, 1:>:-, -:12, <:-1, 0, 1:>, <:0, -1, 1:>:-, -:9, <:1, -1, 1:>, <:0, -1, 1:>:-, -:21, <:1, -1, 1:>, <:1, -1, 2:>:-, -:25, <:1, -1, 2:>, <:2, -2, 2:>:-, -:28, <:1, -2, 2:>, <:2, -2, 2:>:-, -:34, <:1, -2, 2:>, <:1, -2, 1:>:-])

# A++A++A++AB--BABA++AB--BA++ABAB--B--BAB--BAB+
# -ABA++ABA++A++ABAB--BA++AB--BABA++AB--B--B--B


	# prints to the console recursive build instructions for the current solution in l-system format.
	#  https://en.wikipedia.org/wiki/L-system
	def produce_l_system(self):
		rule_a = []
		rule_b = []

		flow_direction = True   # aka choose recursion type A or B? 
		                        # True == A, False == B. With more than 2 rules this will be a cyclical enum

		# build rules
		prev = None
		for s in self.selected_path_stack:
			if prev is not None:
				flow_direction = s.build_l_system(prev, rule_a, rule_b, flow_direction)
			else:
				rule_a.append("A")
				rule_b.append("B")
			prev = s

		# add final direction change to flow with original direction
		# cheating rn, this just always works
		rule_a.append("+")
		rule_b.insert(0, "-")

		print(''.join(rule_a))
		print(''.join(rule_b))


	
	# QUEUEIFY UTILS 

	def binary_search(self, a, x, lo=0, hi=None):
		if hi is None: hi = len(a)
		pos = bisect_left(a, x, lo, hi)                  # find insertion position
		return pos if pos != hi and a[pos] == x else -1  # don't walk off the end

	def find_next(self, l, item):
		if item is None:
			return l[0]
		pos = self.binary_search(l, item)
		if pos == -1:
			print("error :: find_next "+str(item)+" not in list")
		elif pos + 1 == len(l):
			return None 
		else: 
			return l[pos + 1]


	# TESTING UTIL

	# set any solution independent from autosolve
	def set_selected_path_stack(self, new_stack):
		self.selected_path_stack = new_stack


