import generator_flag_graph


# holds all selected flags in order
selected_path_stack = deque()

generator_flag_graph = None

# Coords the path originally emits from 
start_corner_coords = None

# Coords the path currently emits from 
curr_corner_coords = None

numFlags = 7

legal_next_moves = []


def set_up_game(numFlags=7):
	# establish game state
	numFlags = numFlags
	generator_flag_graph = GeneratorFlagGraph(numFlags)
    startCornerCoords = generator_flag_graph.setup(selectedGeneratorFlagsCountdown)
    currCornerCoords = startCornerCoords
    next_flag_options = generator_flag_graph.get_in_play_adjacent_flags(startCornerCoords)

    return generate_flag_state_html()

def generate_flag_state_html():
	all_flags = generator_flag_graph.get_all_flags()
	result = []
	for flag in all_flags:
		result.append("" + flag.)
		