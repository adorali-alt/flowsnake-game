class GeneratorFlag(callbackToAppToAlterPosition) extends React.Component {

  class GeneratorFlagSegmentType {
    static NE = new GeneratorFlagSegmentType('NE');
    static E = new GeneratorFlagSegmentType('E');
    static SE = new GeneratorFlagSegmentType('SE');
  }

  const [selectedSegment, setSelectedSegment] = useState(null);
	const leftCoords = null; // the coords of the left corner of the flag. the other corners are inferred

  constructor(props) {
    super(props);
    this.state = {
      leftCoords: props.c
    };
  }

  // given a corner on this flag, 
  // returns [] of two more flags that will complete this intersection
  spawnAdjacentFlags(c) {
    const result = [];
    if (c.equals(getLeftCoords())) {
      result.push(new GeneratorFlag(c.posIncrW()));
      result.push(new GeneratorFlag(c.posIncrSW()));
    } else if (c.equals(getRightCoords())) {
      result.push(new GeneratorFlag(c);
      result.push(new GeneratorFlag(c.posIncrSW()));
    } else if (c.equals(getTopCoords())) {
      result.push(new GeneratorFlag(c);
      result.push(new GeneratorFlag(c.posIncrW()));
    } else {
        console.log("illegal spawnAdjacentFlags :: corner : " + c + 
          ", on flag with left coords : " + leftCoords);
    }
    return result;
  }

  // given coordinates and a segment type, returns the coords of the segment's other end 
  static getOpposingCoords(c, st) {
    if (c.equals(getLeftCoords())) {
      if (st.equals(GeneratorFlagSegmentType.NE)) {
        return c.posIncrNE();
      } else if (st.equals(GeneratorFlagSegmentType.E)) {
        return c.posIncrE();
      }
    } else if (c.equals(getRightCoords())) {
      if (st.equals(GeneratorFlagSegmentType.SE)) {
        return c.posIncrNW();
      } else if (st.equals(GeneratorFlagSegmentType.E)) {
        return c.posIncrW();
      }
    } else if (c.equals(getTopCoords())) {
      if (st.equals(GeneratorFlagSegmentType.SE)) {
        return c.posIncrSE();
      } else if (st.equals(GeneratorFlagSegmentType.NE)) {
        return c.posIncrSW();
      }
    } 

    console.log("illegal getOpposingCoords :: corner : " + c + 
      ", st : "+ st +", on flag with left coords : " + leftCoords);
    return null;

  }

  getAllCoords() {
    return [getLeftCoords(), getRightCoords(), getTopCoords()];
  }

  getLeftCoords() {
    return leftCoords;
  }

  getRightCoords() {
    return posIncrW(leftCoords);
  }

  getTopCoords() {
    return posIncrNW(leftCoords);
  }

  setSelectedSegment(selectedType) {
    selectedSegment = selectedType;
  }

  selectedCallback(selectedType) {
    if (selectedType == selectedSegment) {
      // this is a deselection 
      setSelectedSegment(null);
      this.props.posUpdateCallback(this, selectedType, false);

    } else if (selectedSegment == null) {
      setSelectedSegment(selectedType);
      this.props.posUpdateCallback(this, selectedType, true);
    }
  }

  return (
    <div>  
      <GeneratorFlagSegment segType=GeneratorFlagSegmentType.NE selectedCallback={this.props.selectedCallback}/>
      <GeneratorFlagSegment segType=GeneratorFlagSegmentType.E selectedCallback={this.props.selectedCallback}/>
      <GeneratorFlagSegment segType=GeneratorFlagSegmentType.SE selectedCallback={this.props.selectedCallback}/>
    </div>
  );
}
