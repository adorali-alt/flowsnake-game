import coords
import generator_flag

# graph class knows about the adjacency of generator flags. new flags are added in groups of 3 in a spiral pattern.
# vertices are corners that 1-3 generator flags may touch
# edges are generator flag segments 
class GeneratorFlagGraph:

	def __init__(self):
		# adjList :: coord -> generator flags with a corner there
        self.adjList = {}
        # ensures getAllFlags() runs quickly after setup()
        self.allFlags = []
        self.startCorner = None # todo this is a global variable cheat 

    # returns [] of flags touching this coord
    def getAdjacentFlags(self, c):
    	# todo try catch block
    	return self.adjList[c]

    # return [] of flags touching this coord which are "in play" available to be selected
    def get_in_play_adjacent_flags(self, c):
    	flags = self.adjList[c]
    	result = []
    	for flag in flags:
    		if flag.isInPlay():
    			result.append(flag)
    	return result

    # given coords of the second to last segment chosen, and the flag dto of the most recent flag chosen, 
    # returns a reference to the most recent flag chosen as it's stored in the graph
    def retrieveFlag(self, last_chosen_coords, flag):
    	flags = get_in_play_adjacent_flags(last_chosen_coords)
    	for f in flags:
    		if f == flag:
    			return f
    	print("retrieveFlag: flag not found, last_chosen_coords = " + last_chosen_coords+", flag = " flag)
    	return 

    # returns [] of all flags in the generator
    def getAllFlags(self):
        if self.allFlags.len() > 0:
            return self.allFlags
        
        map(lambda flag: self.allFlags.append(f), self.adjList.values())
        return self.allFlags

    def getNextFlagOptions(self):
    	return 

    def printGraph(self):
        # get all the vertices
        keys = self.adjList.keys()
     
        # iterate over the vertices
        for coord in keys:
            # get the corresponding adjacency list
            # for the vertex
            flags = self.adjList.get(coord)
            conc = ""
     
            # iterate over the adjacency list
            # concatenate the values into a string
            for flag in flags:
                conc += flag + " "
     
            # print the vertex and its adjacency list
            print(coord + " -> " + conc)


    # setup methods
    def addGeneratorFlag(f):
        flagCoords = f.getAllCoords()
        for c in flagCoords:
            if (!self.adjList.has(c)):
                self.adjList[c] = []
            
            self.adjList.get(c).append(f)
            print("!"+self.adjList.get(c).len())

    def formHexagon(unsaturatedCoords, numOfGeneratorFlags):
        newUnsaturatedCoords = []
        for currCoord in unsaturatedCoords:
            newFlags = GeneratorFlag.spawnAdjacentFlags(currCoord)
            for f in newFlags:
                coordSetSize = self.adjList.keys().len();
                addGeneratorFlag(f);

                diff = self.adjList.keys().len() - coordSetSize
                numOfGeneratorFlags -= diff;
                newUnsaturatedCoords.add(f.getLeftCoords())
                self.startCorner = f

        unsaturatedCoords.clear()
        for c in unsaturatedCoords:
        	unsaturatedCoords.push(c)

        if numOfGeneratorFlags > 0:
            formHexagon(unsaturatedCoords, numOfGeneratorFlags)

    def setup(self, numOfGeneratorFlags):
        # saturated coord == three generator flags
        # unsaturated coord == spot to add the next layer of flags
        unsaturatedCoords = []

        centerFlag = coords.Coords(0, 0, 0)
        unsaturatedCoords.append(centerFlag)
        addGeneratorFlag(generator_flag.GeneratorFlag(centerFlag))

        formHexagon(unsaturatedCoords, numOfGeneratorFlags - 1)

        return self.startCorner

        # todo: add on remainders in a spiral pattern, preserving the invariant:
        # "The shape of the generator flags is symmetric under a 3/2π rotation around its geometrical center."
