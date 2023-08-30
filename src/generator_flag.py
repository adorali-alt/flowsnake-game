from enum import Enum

class GeneratorFlagSegmentType(Enum):
    NE = 1
    E = 2
    SE = 3

class GeneratorFlag:

	def __init__(self, leftCoords):
		# the coords of the left corner of the flag. other corner locations are inferred
    	self.leftCoords = leftCoords 
    	# properties set when a flag is added to the path
    	self.pathSegType = None
    	self.pathEndCoords = None

	# given a coord
	# returns [] of flags that will complete this intersection
	def spawnAdjacentFlags(self, c):
		result = [];
		#left
		result.append(GeneratorFlag(c.posIncrW()))
		result.append(GeneratorFlag(c.posIncrSW()))

		#top
		result.append(GeneratorFlag(c.posIncrNE().posIncrW()))
		result.append(GeneratorFlag(c.posIncrNE().posIncrNE()))

		#right
		result.append(GeneratorFlag(c.posIncrE()))
		result.append(GeneratorFlag(c.posIncrE().posIncrSW()))

		return result

	# given coordinates and a segment type, returns the coords of the segment's other end 
	def getOpposingCoords(self, c, st):
		if c == getLeftCoords():
		    if st.equals(GeneratorFlagSegmentType.NE):
		        return c.posIncrNE()
		    elif st.equals(GeneratorFlagSegmentType.E):
		        return c.posIncrE()
		elif c == getRightCoords():
		    if st.equals(GeneratorFlagSegmentType.SE):
		        return c.posIncrNW()
		    elif st.equals(GeneratorFlagSegmentType.E):
		        return c.posIncrW()
		elif c == getTopCoords():
		    if st.equals(GeneratorFlagSegmentType.SE):
		        return c.posIncrSE()
		    elif st.equals(GeneratorFlagSegmentType.NE):
		        return c.posIncrSW()

		print("illegal getOpposingCoords :: corner : " + c + 
            ", st : "+ st +", on flag with left coords : " + self.leftCoords)
    	return None


	def getAllCoords(self):
		return [getLeftCoords(), getRightCoords(), getTopCoords()]

	def getLeftCoords(self):
		return self.leftCoords

	def getRightCoords(self):
		return self.leftCoords.posIncrW()

	def getTopCoords(self):
		return self.leftCoords.posIncrNW()

	def setFlagAsSelected(self, pathEndCoords, pathSegType):
		self.pathSegType = pathSegType
		self.pathEndCoords = pathEndCoords

	def getPathEndCoords(self):
		return self.pathEndCoords

	def setFlagAsUnselected(self):
		self.pathSegType = None
		self.pathEndCoords = None

	def isInPlay(self):
		return self.pathEndCoords is None and self.pathSegType is None

	def __eq__(self, f):
        return isinstance(obj, f) and f.getLeftCoords() == self.leftCoords
