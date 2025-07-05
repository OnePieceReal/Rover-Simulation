// import axios from 'axios';

// const API_URL = 'http://127.0.0.1:8000';  // Replace with the actual FastAPI server URL

// /*** MAP ENDPOINTS ***/

// // Retrieve the 2D array of the field
// export const getMap = async () => {
//   try {
//     const response = await axios.get(`${API_URL}/map`);
//     console.log("Map:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching map:", error);
//     return null;
//   }
// };

// // Update the height and width of the field
// export const updateMap = async (height, width) => {
//   try {
//     const response = await axios.put(`${API_URL}/map`, null, {
//       params: { height, width },
//     });
//     console.log("Map updated:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error updating map:", error);
//     return null;
//   }
// };

// /*** MINES ENDPOINTS ***/

// // Retrieve all mines
// export const getMines = async () => {
//   try {
//     const response = await axios.get(`${API_URL}/mines`);
//     console.log("Mines:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching mines:", error);
//     return null;
//   }
// };

// // Retrieve a specific mine by ID
// export const getMine = async (mineId) => {
//   try {
//     const response = await axios.get(`${API_URL}/mines/${mineId}`);
//     console.log("Mine:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching mine:", error);
//     return null;
//   }
// };

// // Create a mine
// export const createMine = async (serialNumber, x, y) => {
//   try {
//     const response = await axios.post(`${API_URL}/mines`, null,{params:{ serial_number: serialNumber, x, y }});
//     console.log("Mine created:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error creating mine:", error);
//     return null;
//   }
// };

// // Update a mine
// export const updateMine = async (mineId, serialNumber = null, x = null, y = null) => {
//   try {
//     // Construct query parameters object
//     const params = {};

//     // Add serialNumber, x, and y to the params if they are provided
//     if (serialNumber !== null) {
//       params.serial_number = serialNumber;
//     }

//     if (x !== null) {
//       params.x = x;
//     }

//     if (y !== null) {
//       params.y = y;
//     }

//     // Make the PUT request to update the mine, passing the params as query parameters
//     const response = await axios.put(`${API_URL}/mines/${mineId}`, null, { params });
    
//     console.log("Mine updated:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error updating mine:", error);
//     return null;
//   }
// };

// // Delete a mine
// export const deleteMine = async (mineId) => {
//   try {
//     const response = await axios.delete(`${API_URL}/mines/${mineId}`);
//     console.log("Mine deleted:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error deleting mine:", error);
//     return null;
//   }
// };

// /*** ROVERS ENDPOINTS ***/

// // Retrieve all rovers
// export const getRovers = async () => {
//   try {
//     const response = await axios.get(`${API_URL}/rovers`);
//     console.log("Rovers:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching rovers:", error);
//     return null;
//   }
// };

// // Retrieve a specific rover by ID
// export const getRover = async (roverId) => {
//   try {
//     const response = await axios.get(`${API_URL}/rovers/${roverId}`);
//     console.log("Rover:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching rover:", error);
//     return null;
//   }
// };

// // Create a rover
// export const createRover = async (commands) => {
//   try {
//     const response = await axios.post(`${API_URL}/rovers`,null,{ params:{ commands: commands }});
//     console.log("Rover created:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error creating rover:", error);
//     return null;
//   }
// };

// // Delete a rover
// export const deleteRover = async (roverId) => {
//   try {
//     const response = await axios.delete(`${API_URL}/rovers/${roverId}`);
//     console.log("Rover deleted:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error deleting rover:", error);
//     return null;
//   }
// };

// // Update rover commands
// export const updateRoverCommands = async (roverId, commands) => {
//   try {
//     const response = await axios.put(`${API_URL}/rovers/${roverId}`, null,{params:{ commands }});
//     console.log("Rover commands updated:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error updating rover commands:", error);
//     return null;
//   }
// };

// // Dispatch a rover
// export const dispatchRover = async (roverId) => {
//   try {
//     const response = await axios.post(`${API_URL}/rovers/${roverId}/dispatch`, null, {
//       timeout: 300000  // Timeout set to 300 milliseconds
//     });
//     // console.log("Rover dispatched:", response.data);
//     return response.data;
//   } catch (error) {
//     console.error("Error dispatching rover:", error);
//     return null;
//   }
// };


// //testing the above endpoints 
// function testMap(){
//   getMap();
//   updateMap(4,4);
//   getMap();
// }
// //testMap();

// async function testMines() {
//   try {
//     // Uncomment the lines that you want to execute in sequence  
//     await getMines();  // Assuming this is an async function
//     await getMine(1);  // Assuming this is an async function
//     await createMine("M123", 0, 0);  // Make sure this is an async function
//     await getMines();
//     await deleteMine(3);  // Make sure this is an async function
//     await getMines();
//     await updateMine(2, null, 2, 2);  // Make sure this is an async function
//     await getMines(); 
//   } catch (error) {
//     console.error("Error in testMines:", error);
//   }
// }
// // testMines();

// async function testRover(){
//   await getRovers();
//   await getRover(2);
//   await createRover("LLLLLLLLLL");
//   await getRovers();
//   await deleteRover(11)
//   await updateRoverCommands(10,"RRRRRR")
//   await getRovers();
//   await dispatchRover(2);
// }
// // testRover();
