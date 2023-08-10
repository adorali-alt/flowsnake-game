// graph class knows about the adjacency of generator flags. new flags are added in groups of 3 in a spiral pattern.

// vertices are corners that 1-3 generator flags may touch
// edges are generator flag segments 
class GeneratorFlagGraph {

    const AdjList = null;

    const allFlags = new Set();

    constructor() {
        // map :: coord -> generator flags with a corner there
        this.AdjList = new Map();
    }

    setup(numOfGeneratorFlags) {
        // saturated coord == three generator flags
        // unsaturated coord == spot to add the next layer of flags
        const unsaturatedCoords = [];
        let center = new Coords(0, 0, 0);
        unsaturatedCoords.push(center);
        formHexagon(unsaturatedCoords, numOfGeneratorFlags);

        // todo: add on remainders in a spiral pattern, preserving the invariant:
        // "The shape of the generator flags is symmetric under a 3/2π rotation around its geometrical center."
    }

    // helper
    formHexagon(unsaturatedCoords, numOfGeneratorFlags) {
        const newUnsaturatedCoords = new Set();
        unsaturatedCoords.forEach(function(currCoord) {
            let newFlags = spawnAdjacentFlags(currCoord);
            let numofNewFlags = 0;
            generatorFlags.forEach(function(f) { 
                let coordSetSize = this.AdjList.size();
                addGeneratorFlag(f);
                if (coordSetSize < this.AdjList.size()) {
                    numOfGeneratorFlags -= 1;
                }
                newUnsaturatedCoords.add(f.getLeftCoords());
            });
        });

        unsaturatedCoords.dump();
        unsaturatedCoords.addAll(newUnsaturatedLocationCoords);

        if (numOfGeneratorFlags > 0) {
            formHexagon(unsaturatedCoords, numOfGeneratorFlags);
        }
    }
     
    addGeneratorFlag(f) {
        const flagCoords = f.getAllCoords();
        flagCoords.forEach(function (c) {
            if (!this.AdjList.has(c)) {
                this.AdjList.set(c, new Set());
            }
            this.AdjList.get(c).add(f);
        });

    }

    // returns [] of flags touching this coord
    getAdjacentFlags(currLocation) {
        this.AdjList.get(currLocation);
    }

    getAllFlags() {
        if (allFlags.size() > 0) {
            return allFlags;
        }
        this.AdjList.get.values().forEach(function(f) {
            allFlags.add(f);
        });
        return allFlags;
    }

    // for debugging
    printGraph() {
        // get all the vertices
        var get_keys = this.AdjList.keys();
     
        // iterate over the vertices
        for (var i of get_keys) {
            // get the corresponding adjacency list
            // for the vertex
            var get_values = this.AdjList.get(i);
            var conc = "";
     
            // iterate over the adjacency list
            // concatenate the values into a string
            for (var j of get_values)
                conc += j + " ";
     
            // print the vertex and its adjacency list
            console.log(i + " -> " + conc);
        }
    }
}