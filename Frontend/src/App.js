import React from "react";
import { useState, useEffect } from "react";
import MinesTable from "./components/MinesTable";
import RoversTable from "./components/RoversTable";
import MapDisplay from "./components/MapDisplay";
import ResultsDisplay from "./components/ResultsDisplay";

function App() {
  const [updateMapFlag, setMapUpdateFlag] = useState(false);
  const [updateMineFlag,setMineUpdateFlag] =useState(false);
  const [dispatchResults,setDispatchResults] = useState(null);

  const handleMineUpdateFlag = () =>{
    setMineUpdateFlag((prev)=> !prev)
  }
  const handleMapUpdateFlag = () => {
    setMapUpdateFlag((prev) => !prev); 
  };
  const setRoverResults=(results)=>{
    setDispatchResults(results) 
  }
  return (
    <div className="App bg-gray-900 text-white min-h-screen p-4">
      <MapDisplay handleMapUpdateFlag={handleMapUpdateFlag} updateMineFlag={updateMineFlag} />
      <MinesTable updateMapFlag={updateMapFlag} handleMineUpdateFlag={handleMineUpdateFlag}/>
      <RoversTable setRoverResults={setRoverResults} updateMineFlag={updateMineFlag} updateMapFlag={updateMapFlag}/>
      <ResultsDisplay dispatchResults={dispatchResults} />
    </div>
  );
}


export default App;
