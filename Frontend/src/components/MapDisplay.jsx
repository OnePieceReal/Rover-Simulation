import { useState, useEffect } from "react";
import * as api from "../api";

export default function MapDisplay({handleMapUpdateFlag, updateMineFlag}) {
  const [map, setMap] = useState([]);
  const [height, setHeight] = useState(0);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    fetchMap();
  }, [updateMineFlag]);

  const fetchMap = async () => {
    const data = await api.getMap();
    if (data) {
      setMap(data.map);
      setHeight(data.map.length);
      setWidth(data.map[0]?.length || 0);
    }
  };

  const handleResize = async (deltaH, deltaW) => {
    const newHeight = Math.max(1, height + deltaH);
    const newWidth = Math.max(1, width + deltaW);

    const updatedMap = Array.from({ length: newHeight }, (_, i) =>
      Array.from({ length: newWidth }, (_, j) =>
        i < height && j < width ? map[i][j] : "0"
      )
    );

    setMap(updatedMap);
    setHeight(newHeight);
    setWidth(newWidth);
    await api.updateMap(newHeight, newWidth);
    handleMapUpdateFlag()
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-gray-900 text-white shadow-lg rounded-lg text-center">
      <h3 className="text-2xl font-semibold mb-4">Rover Map</h3>
      <div className="overflow-auto border border-gray-700 rounded-lg">
        <table className="w-full border-collapse">
          <tbody>
            {map.map((row, rowIndex) => (
              <tr key={rowIndex} className="border">
                {row.map((cell, colIndex) => (
                  <td
                    key={colIndex}
                    className={`w-12 h-12 text-center font-bold border ${
                      cell === "1" ? "bg-gray-800 text-white" : "bg-gray-600 text-white"
                    }`}
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 space-x-2">
        <button
          onClick={() => handleResize(1, 1)}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 shadow-md"
        >
          +
        </button>
        <button
          onClick={() => handleResize(-1, -1)}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 shadow-md"
        >
          -
        </button>
      </div>
    </div>
  );
}
