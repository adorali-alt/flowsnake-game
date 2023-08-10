// Coords objects are immutable
class Coords() {
	// (x,y,z) coordinates mapped to an isometric hex grid, with x = /, y = |, z = \

	const x = 0;
	const y = 0;
	const z = 0;

	constructor(x, y, z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	posIncrN(c) {
		return new Coords(c.x, c.y + 1, c.z);
	} 
	posIncrNE(c) {
		return new Coords(c.x + 1, c.y, c.z);
	} 
	posIncrSE(c) {
		return new Coords(c.x, c.y, c.z - 1);
	}
	posIncrS(c) {
		return new Coords(c.x, c.y - 1, c.z);
	}
	posIncrSW(c) {
		return new Coords(c.x - 1, c.y, c.z);
	} 
	posIncrW(c) {
		return new Coords(c.x - 1, c.y, c.z + 1);
	} 
	posIncrNW(c) {
		return new Coords(c.x, c.y, c.z + 1);
	}

	equals(c) {
		return c.x == this.x && c.y == this.y && c.z == this.z;
	}
}