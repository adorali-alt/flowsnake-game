// generator flag segments can be "selected". selecting means adding that edge to the flowsnake path. 
// When one generator flag's edge is selected, then that flag's other two edges are unselectable. They'll 
// become unlit in the UI.

class GeneratorFlagSegment() extends React.Component {
  const coords = [];
  // const isInFlowsnake = false;
  // const isOutOfPlay = false;

  constructor(props) {
    super(props);
    this.state = {
      coords: props.coords
    };
  }

  // function elementWasClicked() {
  //   isInFlowsnake = !isInFlowsnake;
  // }

  // getSegType() {
  //   return this.props.segType;
  // }

  // returnToPlay() {
  //   isOutOfPlay = false;
  //   isInFlowsnake = false;
  // }

  // removeFromPlay() {
  //   isOutOfPlay = true;
  // }

  // addToFlowsnake() {
  //   isInFlowsnake = true;
  // }

  getCoords() {
    return coords;
  }

  render() {
    return (
      <div className="flagSegment" onClick={() => {
              this.props.selectedCallback(this.props.segType)}}}>
          <figure>
              <img src={this.props.segType+"-segment.jpg"} alt={this.props.segType} aria-labelledby={this.props.segType}/>
          </figure>
      </div>);
  }
}