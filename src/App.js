import './index.css';

export default function FlowsnakeGame() {

    const numOfGeneratorFlags = 7; // todo: add a function for user input
    const [currLocation, setCurrLocation] = useState(CurrLocationObject(0, 0, 0));
    const [nextFlagOptions, setNextFlagOptions] = useState([]);

    const generatorFlagGraph = new GeneratorFlagGraph();

    // LIFE CYCLE METHODS ------------------

    componentDidMount() {
        generatorFlagGraph.setup(numOfGeneratorFlags);        
    }


    // CALL BACK FUNCTIONS ------------------

    // Update the next flags given the currLocation
    setNextFlagOptions() {
        nextFlagOptions = generatorFlagGraph.getAdjacentFlags(currLocation);
    }

    // Update the user's active location when they select or de-select a segment 
    setCurrLocation(st) {
        currLocation = GeneratorFlag.getOpposingCoords(currLocation, st);
    }

    render() {
        let gfSet = generatorFlagGraph.getAllFlags();
        // display as a list, have flags render themselves by rotation. rerender one flag upon update
        
        return (
            <div className="flag">  
              <GeneratorFlag posUpdateCallback={(st) => this.setCurrLocation(st)}/>
            </div>
        );
    }

}

export default App;
