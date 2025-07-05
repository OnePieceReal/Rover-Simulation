import { useState, useEffect } from "react";
import * as api from "../api";
import ErrorCard from "./ErrorCard";
export default function MinesTable({ updateMapFlag, handleMineUpdateFlag }) {
  const [mines, setMines] = useState([]);
  const [newSerialNumber, setNewSerialNumber] = useState("");
  const [newPosition, setNewPosition] = useState("");
  const [displayErrorFlag, setErrorFlag] = useState(false)

  const handleError = () =>{
    setErrorFlag((displayErrorFlag)=>!displayErrorFlag)
  }

  useEffect(() => {
    // console.log("flag changed")
    fetchMines();
  }, [updateMapFlag]);

  const fetchMines = async () => {
    try {
      const response = await api.getMines();
      const data = JSON.parse(response);
      const formattedMines = data.map((mine) => ({
        ...mine,
        editable: false,
      }));
      setMines(formattedMines);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleDelete = async (id) => {
    if(!(mines.find((mine)=> mine.id === id))) return;
    const response = await api.deleteMine(id);
    if(!response) return;  
    setMines(mines.filter((mine) => mine.id !== id));
    handleMineUpdateFlag();
  };

  const handleUpdate = async (id) => {
    const mineToUpdate = mines.find((mine) => mine.id === id);
    if (!mineToUpdate) {
      if(!displayErrorFlag)handleError();
      return;
    }
  
    if (mineToUpdate.editable) { // Save mode
      const [x, y] = mineToUpdate.position.split(",");
      const x_int = parseInt(x, 10);
      const y_int = parseInt(y, 10);
  
      if (mineToUpdate.position && mineToUpdate.serial_number && x_int >= 0 && y_int >= 0) {
        const response = await api.updateMine(mineToUpdate.id, mineToUpdate.serial_number, x_int, y_int);
        if (!response) {
          if(!displayErrorFlag)handleError();
          return;
        } // Prevent UI update if API request fails
        handleMineUpdateFlag();
      } else {
        return; // Invalid input, don't toggle
      }
    }
 
    setMines(
      mines.map((mine) =>
        mine.id === id ? { ...mine, editable: !mine.editable } : mine
      )
      .sort((a, b) => a.id - b.id)
    );
    if(displayErrorFlag && mineToUpdate.editable)handleError();
  };
  
  const handleChange = (id, field, value) => {
    setMines(
      mines.map((mine) =>
        mine.id === id ? { ...mine, [field]: value } : mine
      )
    );
  };

  const handleAddMine = async () => {
    if (newSerialNumber && newPosition) {
      const [x, y] = newPosition.split(",");
      const newMine = await api.createMine(newSerialNumber, parseInt(x, 10), parseInt(y, 10));
      if (!newMine){
        if(!displayErrorFlag)handleError();
        return;
      }
      setMines([...mines, { id: newMine["mine_id"], serial_number: newSerialNumber, position: newPosition, editable: false }]);
      setNewSerialNumber("");
      setNewPosition("");
      handleMineUpdateFlag();
    }
    else{
      if(!displayErrorFlag)handleError();
      return;
    }
    if(displayErrorFlag)handleError();
  };

  return (
   
    <div className="p-6 max-w-4xl mx-auto bg-gray-900 text-white shadow-lg rounded-lg">
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-4">Add New Mine</h2>
        <div className="flex space-x-4">
        <input
        type="text"
        placeholder="Serial Number"
        value={newSerialNumber}
        onChange={(e) => setNewSerialNumber(e.target.value)}
        className="w-full md:w-2/3 p-3 bg-gray-700 border border-gray-600 rounded-lg shadow-md text-white focus:outline-none focus:ring-2 focus:ring-green-500"
      />

      <input
        type="text"
        placeholder="X,Y"
        value={newPosition}
        onChange={(e) => setNewPosition(e.target.value)}
        className="w-full md:w-1/3 p-3 bg-gray-700 border border-gray-600 rounded-lg shadow-md text-white focus:outline-none focus:ring-2 focus:ring-green-500"
      />

      <button
        onClick={handleAddMine}
        className="px-6 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
      >
        Add Mine
      </button>

        </div>
      </div>
      <ErrorCard message={"Invalid Input! Please try again!"} displayErrorFlag={displayErrorFlag} handleError={handleError} className="mb-4"/>
      
      <table className="w-full border-collapse border border-gray-700 text-center">
        <thead>
          <tr className="bg-gray-800 text-gray-300">
            <th className="border border-white p-3">ID</th>
            <th className="border border-white p-3">Serial Number</th>
            <th className="border border-white p-3">Position</th>
            <th className="border border-white p-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          {mines.map((mine) => (
            <tr key={mine.id} className="border hover:bg-gray-700">
              <td className="border p-3">{mine.id}</td>
              <td className="border p-3">
                {mine.editable ? (
                  <input
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded text-white"
                    value={mine.serial_number}
                    onChange={(e) => handleChange(mine.id, "serial_number", e.target.value)}
                  />
                ) : (
                  mine.serial_number
                )}
              </td>
              <td className="border p-3">
                {mine.editable ? (
                  <input
                    className="w-full p-2 bg-gray-800 border border-gray-600 rounded text-white"
                    value={mine.position}
                    onChange={(e) => handleChange(mine.id, "position", e.target.value)}
                  />
                ) : (
                  mine.position
                )}
              </td>
              <td className="border p-3">
                <button
                  onClick={() => handleUpdate(mine.id)}
                  className="mr-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                  {mine.editable ? "Save" : "Update"}
                </button>
                <button
                  onClick={() => handleDelete(mine.id)}
                  className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
