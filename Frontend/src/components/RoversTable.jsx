import { useState, useEffect } from "react";
import * as api from "../api";
import ErrorCard from "./ErrorCard";
export default function RoversTable({setRoverResults,updateMineFlag, updateMapFlag}) {
  const [rovers, setRovers] = useState([]);
  const [newCommand, setNewCommand] = useState("");
  const [displayErrorFlag, setErrorFlag] = useState(false)
  useEffect(() => {
    fetchRovers();
  }, [updateMineFlag,updateMapFlag]);

  const fetchRovers = async () => {
    try {
      const response = await api.getRovers();
      const data = JSON.parse(response);
      const formattedRovers = data.map((rover) => ({
        ...rover,
        editable: false,
      }));
      setRovers(formattedRovers);
    } catch (error) {
      console.error("Error fetching rovers:", error);
    }
  };

  const handleError = () =>{
    setErrorFlag((displayErrorFlag)=>!displayErrorFlag)
  }

  const handleDelete = async (id) => {
    if(!rovers.find((rover)=> rover.id ===id)) return
    const response = await api.deleteRover(id)
    if(!response) return;
    setRovers(rovers.filter((rover) => rover.id !== id));
  };

  const handleUpdate = async (id) => {
    const roverToUpdate = rovers.find((rover) => rover.id === id);
    if (!roverToUpdate) return;
  
    if (roverToUpdate.editable) { // Save mode
      if (!roverToUpdate.commands) {
        if(!displayErrorFlag)handleError();
        return; // prevent empty command updates
      }
      const response = await api.updateRoverCommands(roverToUpdate.id, roverToUpdate.commands);
      if (!response){
        if(!displayErrorFlag)handleError();
        return; // prevent empty command updates
      } 
    }
    setRovers(
      rovers.map((rover) =>
        rover.id === id ? { ...rover, editable: !rover.editable } : rover
      )
    );
    if(displayErrorFlag)handleError();
  };
  

  const handleChange = (id, value) => {
    setRovers(
      rovers.map((rover) =>
        rover.id === id ? { ...rover, commands: value } : rover
      )
    );
  };

  const handleAddRover = async () => {
    if(!newCommand) {
      if(!displayErrorFlag)handleError();
      return;
    }
    const response = await api.createRover(newCommand);
    if(!response) {
      if(!displayErrorFlag)handleError();
      return;
    }
    const newRover = {
        id: response["id"],
        commands: newCommand,
        status: "Not Started",
        editable: false,
      };
    setRovers((prevRovers) => [...prevRovers, newRover]);
    setNewCommand(""); 
    if(displayErrorFlag)handleError();
  };

  const handleDispatch = async (id) => {
    try {
      const response = await api.dispatchRover(id);
      const data = JSON.parse(response);
      // console.log(response);
      // console.log(data.id);
      setRoverResults({
        id: data.id,
        status: data.status,
        position: data.position,
        executed_commands: data.executed_commands,
        map: data.map,
      });
      setRovers(rovers.map((rover)=>rover.id === id? {...rover, status: data.status}:rover))
    } catch (error) {
      console.error("Error dispatching rover:", error);
    }
  };
  

  return (
    <div className="p-6 max-w-4xl mx-auto bg-gray-900 text-white shadow-lg rounded-lg">
      <h3 className="text-xl font-semibold mb-4">Add New Rover</h3>
      <div className="flex gap-2 mb-4">
      <input
  className="w-full p-3 bg-gray-700 text-white border border-gray-600 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
  placeholder="Enter rover commands"
  value={newCommand}
  onChange={(e) => setNewCommand(e.target.value)}
/>

<button
  onClick={handleAddRover}
  className="px-6 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
>
  Add Rover
</button>
      
      </div>
    
      <ErrorCard message={"Invalid Input! Please try again!"} displayErrorFlag={displayErrorFlag} handleError={handleError} className="mb-4"/>

      <table className="w-full border-collapse text-center">
        <thead>
          <tr className="bg-gray-800">
            <th className="border border-white p-3">ID</th>
            <th className="border border-white p-3">Commands</th>
            <th className="border border-white p-3">Status</th>
            <th className="border border-white p-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rovers.map((rover) => (
            <tr key={rover.id} className="border border-white hover:bg-gray-800">
              <td className="border border-white p-3">{rover.id}</td>
              <td className="border p-3 text-xs break-words max-w-xs">
                {rover.editable ? (
                    <textarea
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded text-white"
                    value={rover.commands || ""}
                    onChange={(e) => handleChange(rover.id, e.target.value)}
                    />
                ) : (
                    rover.commands ? rover.commands.match(/.{1,50}/g).join("\n") : "No Commands"
                )}
                </td>

              <td className="border border-white p-3">{rover.status}</td>
              <td className="border border-white p-3">
                <button
                  onClick={() => handleUpdate(rover.id)}
                  className="mr-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  {rover.editable ? "Save" : "Update"}
                </button>
                <button
                  onClick={() => handleDelete(rover.id)}
                  className="mr-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Delete
                </button>
                <button
                  onClick={() => handleDispatch(rover.id)}
                  className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                >
                  Dispatch
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
