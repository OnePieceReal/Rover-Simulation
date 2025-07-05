import React from "react";

export default function ResultsDisplay({ dispatchResults }) {
  if (!dispatchResults) {
    
    return (
      <div className="p-6 max-w-4xl mx-auto bg-gray-900 text-white shadow-lg rounded-lg"><h3 className="text-xl font-semibold mb-4">Dispatch Result</h3>
      <p className="text-gray-400 text-center">Click "Dispatch" to show result!</p></div>
   
    );
  }

  const { id, status, position, executed_commands, map } = dispatchResults;

  const formatCommands = (commands) => {
    if (!commands) return "No Commands";
    return commands.match(/.{1,50}/g).join("\n"); 
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-gray-900 text-white shadow-lg rounded-lg">
      <h3 className="text-xl font-semibold mb-4">Dispatch Result</h3>

      <table className="w-full border-collapse text-left">
        <tbody>
          <tr className="border border-white">
            <th className="border border-white p-3 bg-gray-800 w-1/3">Rover ID</th>
            <td className="border border-white p-3">{id}</td>
          </tr>
          <tr className="border border-white">
            <th className="border border-white p-3 bg-gray-800">Status</th>
            <td className="border border-white p-3">{status}</td>
          </tr>
          <tr className="border border-white">
            <th className="border border-white p-3 bg-gray-800">Position</th>
            <td className="border border-white p-3">{position}</td>
          </tr>
          <tr className="border border-white">
            <th className="border border-white p-3 bg-gray-800">Executed Commands</th>
            <td className="border border-white p-3 text-xs break-words whitespace-pre-wrap">
              {formatCommands(executed_commands)}
            </td>
          </tr>
        </tbody>
      </table>

      {map ? (
        <div className="overflow-auto border border-gray-700 rounded-lg mt-4">
          <table className="w-full border-collapse">
            <tbody>
              {map.map((row, rowIndex) => (
                <tr key={rowIndex} className="border">
                  {row.map((cell, colIndex) => (
                    <td
                      key={colIndex}
                      className={`w-12 h-12 text-center font-bold border p-2 ${
                        cell === "*"
                          ? "bg-cyan-500 text-white" // For "*" cells (cyan)
                          : cell === "0"
                          ? "bg-gray-700 text-white" // For "0" cells (dark gray)
                          : cell > 0
                          ? "bg-gray-800 text-white" // For values > 0 (slightly lighter gray)
                          : "bg-gray-600 text-white" // Default for unknown cases
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
      ) : (
        <p className="text-gray-400 mt-4">No map data available</p>
      )}
    </div>
  );
}
