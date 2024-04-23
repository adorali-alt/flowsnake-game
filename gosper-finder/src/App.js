import React, { useState, useEffect } from 'react';

import './App.css';
import { Canvas } from "@react-three/fiber";
import { Environment, OrbitControls } from "@react-three/drei";

function App() {

  const [model, setModel] = useState(0);

  useEffect(() => {
    fetch('/model').then(res => res.json()).then(data => {
      setModel(data.model);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p> behold, the data we have received is {model}. Spin the model to get a better look. </p>
        <p> source code </p>
        <p> written explanation </p>
      </header>
      <Canvas camera={{fov: 18}}>
        <ambientLight intensity={1.25}/>
        <mesh>
          <boxGeometry />
          <meshStandardMaterial color="green"/>
        </mesh>
        <Environment preset="sunset" />
        <OrbitControls />
      </Canvas>
    </div>
  );
}

export default App;
