from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from typing import List, Dict
import RoverSimulation
import json
import random
import copy
import os
app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (use specific headers in production)
)

rover_map = RoverSimulation.create_map()
mine_snum_pos_dict ={}
mine_id_pos_dict={}
mine_tag=0
rovers_dict ={}
#convert the array of rovers to a dictionary
def rovers_to_dict():
    global rovers_dict
    all_rovers =RoverSimulation.initialize_rovers()
    for rover in all_rovers:
        rovers_dict[rover.id] = rover
rovers_to_dict()
rover_id_count=len(rovers_dict)
# To retrieve the list of all rovers, the response should at least
# include the ID and rover status (“Not Started”, “Finished”,
# “Moving”, or “Eliminated”).
def get_all_rovers_json():
    global rovers_dict
    rover_list=[]
    for rover_id, rover in rovers_dict.items():
        rover_info = {
            "id": rover_id,
            "commands":rover.moves,
            "status": rover.status
        }
        rover_list.append(rover_info)
    return json.dumps(rover_list, indent=4)

#function to get all mines in the map w/ their serial number and coordinates
def load_mine_data():
    global rover_map, mine_snum_pos_dict, mine_id_pos_dict, mine_tag
    with open(RoverSimulation.MINE_TXT_FILE_LOCATION, 'r') as file:
        mine_serial_numbers = [line.strip() for line in file]
    map_data = rover_map
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j].isdigit() and int(map_data[i][j]) > 0 and (str(i)+","+str(j)) not in mine_snum_pos_dict:
                mine_tag += 1
                mine_serial = mine_serial_numbers[mine_tag % (len(mine_serial_numbers)-1)]
                mine_snum_pos_dict[str(i)+","+str(j)] = mine_serial
                mine_id_pos_dict[mine_tag] = str(i)+","+str(j)
    return  mine_snum_pos_dict, mine_id_pos_dict
load_mine_data()
# Function to resize the map
def resize_map(original_map, new_height, new_width):
    resized_map = original_map[:new_height]
    resized_map = [row[:new_width] for row in resized_map]
    while len(resized_map) < new_height:
        resized_map.append(['0'] * new_width)
    resized_map = [
        row + ['0'] * (new_width - len(row)) for row in resized_map
    ]
    return resized_map

#convert mine dictionary to the necessary format so that the rover can understand
def convert_mine_dic():
    global mine_snum_pos_dict
    new_dict = {}
    # Iterate over the mine_id_pos_dict to convert the keys and keep the values
    for key, value in mine_snum_pos_dict.items():
        # Convert the key (string) into a tuple by splitting and converting to integers
        x,y= map(int, key.split(','))
        new_dict[(x,y)] = value
    return new_dict

#update the rover mines based on the updated rover map
def update_mine_based_on_map():
    global rover_map, mine_snum_pos_dict, mine_id_pos_dict

    rows = len(rover_map)
    columns = len(rover_map[0])

    keys_to_delete = []

    for key, values in mine_id_pos_dict.items():
        x, y = map(int, values.split(','))
        if x >= rows or y >= columns:
            keys_to_delete.append(key)

    for key in keys_to_delete:
        values = mine_id_pos_dict[key]
        del mine_id_pos_dict[key]
        del mine_snum_pos_dict[values]

#update all rover maps
def update_map_rovers():
    global rover_map, rovers_dict
    for rover_id,rover in rovers_dict.items():
        if rover.status != "Moving":
            rover.map = copy.deepcopy(rover_map)
            rover.reset()
        else:
            rover.map_update_status=True
            rover.backup_map = copy.deepcopy(rover_map)

#check the validity of the commands
def check_commands(commands):
    if not commands:  # Covers both None and empty string/list
        return False
    for command in commands:
        if command not in ['L', 'R', 'D', 'M']:
            return False
    return True

def check_for_mine_update_collisions(id,x,y):
    global mine_id_pos_dict
    for key,value in mine_id_pos_dict.items():
        if key != id and (str(x)+","+str(y)) == value:
            return True
    return False

"""Map endpoints"""
#to retrieve the 2D array of the field.
@app.get("/map")
def get_map():
    global rover_map
    return {"map": rover_map}

#To update the height and width of the field.
@app.put("/map")
def update_map(height: int, width: int):
    global rover_map # Access the global variable
    rover_map = resize_map(rover_map, height, width)  # Resize the map to new height and width
    update_map_rovers()
    update_mine_based_on_map()
    return {"message": "Map updated successfully"}

"""Mine enpoints"""
# To retrieve the list of all mines, the response should include
# the serial number of the mines, and coordinates
@app.get("/mines")
def get_mines():
    global mine_snum_pos_dict, mine_id_pos_dict

    # To retrieve a mine with the “:id”, the response should
    # include the serial number of the mine, and coordinates
    load_mine_data()
    mines=[]
    for key,value in mine_id_pos_dict.items():
        mine_info={
            "id":key,
            "position":value,
            "serial_number":mine_snum_pos_dict[value]
        }
        mines.append(mine_info)
    return json.dumps(mines, indent=4)

@app.get("/mines/{mine_id}")
def get_mine(mine_id: int):
    global mine_snum_pos_dict, mine_id_pos_dict
    if mine_id not in mine_id_pos_dict:
        raise HTTPException(status_code=404, detail="Mine not found")
    mine_pos = mine_id_pos_dict[mine_id]
    return {mine_pos:mine_snum_pos_dict[mine_pos]}

# To delete a mine with the “:id”
@app.delete("/mines/{mine_id}")
def delete_mine(mine_id: int):
    global mine_snum_pos_dict, mine_id_pos_dict, rover_map
    if mine_id not in mine_id_pos_dict:
        raise HTTPException(status_code=404, detail="Mine not found")
    mine_pos = mine_id_pos_dict[mine_id]
    x, y = map(int, mine_pos.split(","))
    rover_map[x][y]='0'
    del mine_id_pos_dict[mine_id]
    del mine_snum_pos_dict[mine_pos]
    update_map_rovers()
    return {"message": "Mine deleted successfully"}

# To create a mine. The coordinates (X and Y), along with the
# serial number should be required in the body of the request.
# The ID of the mine should be returned in the response upon
# successful creation.
@app.post("/mines")
def create_mine(serial_number: str, x: int, y: int):
    global rover_map, mine_snum_pos_dict, mine_id_pos_dict, mine_tag
    mine_pos = str(x)+","+str(y)
    if mine_pos in mine_snum_pos_dict:
        raise HTTPException(
            status_code=409,
            detail=f"Mine already exists in that location"
        )
    if x >= len(rover_map) or y >= len(rover_map[0]) or x < 0 or y <0:
        raise HTTPException(
            status_code=400,
            detail="Coordinates out of bounds. Please provide valid coordinates within the map."
        )
    mine_tag+=1
    rover_map[x][y]='1'
    mine_id_pos_dict[mine_tag]=mine_pos
    mine_snum_pos_dict[mine_pos] =serial_number
    update_map_rovers()
    return {"mine_id":mine_tag}

# To update a mine. The coordinates (X and Y), along with
# the serial number should be optional in the body of the
# request. Only the included parameters should get updated
# upon receiving the request. The response must include the
# full updated mine object.
@app.put("/mines/{mine_id}")
def update_mine(mine_id: int, serial_number: str = None, x: int = None, y: int = None):
    global rover_map, mine_snum_pos_dict, mine_id_pos_dict
    mine_pos=""
    if mine_id not in mine_id_pos_dict:
        raise HTTPException(status_code=404, detail="Mine not found")
    if serial_number is None and (x is None or y is None):
        raise HTTPException(status_code=400, detail="Missing required parameters")
    if x is not None and y is not None:
        if x >= len(rover_map) or y >= len(rover_map[0]) or x <0 or y<0:
            raise HTTPException(
                status_code=400,
                detail="Coordinates out of bounds. Please provide valid coordinates within the map."
            )
        if check_for_mine_update_collisions(mine_id,x,y):
            raise HTTPException(
                status_code=409,
                detail=f"Mine already exists in that location"
            )
        mine_pos=str(x)+","+str(y)
        initial_pos = mine_id_pos_dict[mine_id]
        mine_serial =mine_snum_pos_dict[initial_pos]
        x_i,y_i = map(int, initial_pos.split(","))
        rover_map[x_i][y_i]='0'
        rover_map[x][y] = '1'
        del mine_id_pos_dict[mine_id]
        del mine_snum_pos_dict[initial_pos]
        mine_id_pos_dict[mine_id]=mine_pos
        mine_snum_pos_dict[mine_pos]=mine_serial
        update_map_rovers()
    if serial_number is not None:
        mine_pos=mine_id_pos_dict[mine_id]
        mine_snum_pos_dict[mine_pos]=serial_number
    return {mine_pos:mine_snum_pos_dict[mine_pos]}

"""Rovers Endpoints"""
# To retrieve the list of all rovers, the response should at least
# include the ID and rover status (“Not Started”, “Finished”,
# “Moving”, or “Eliminated”).
@app.get("/rovers")
def get_rovers():
    return get_all_rovers_json()

# To retrieve a rover with the “:id”, the response should
# include the ID, status (“Not Started”, “Finished”, “Moving”, or
# “Eliminated”), latest position and list of commands of the
# rover
@app.get("/rovers/{rover_id}")
def get_rover(rover_id: int):
    global rovers_dict
    if rover_id not in rovers_dict:
        raise HTTPException(status_code=404, detail="Rover not found")
    rover =rovers_dict[rover_id]
    rover_info={
        "id":rover_id,
        "status":rover.status,
        "position":str(rover.x)+","+str(rover.y),
        "commands":rover.moves
    }
    return  json.dumps(rover_info, indent=4)

# To create a rover. The list of commands as a String should
# be required in the body of the request. The ID of the rover
# should be returned in the response upon successful
# creation.
@app.post("/rovers")
def create_rover(commands: str):
    global rover_id_count,rovers_dict, rover_map
    if not check_commands(commands):
        raise HTTPException(status_code=400, detail="Commands invalid")
    rover_id_count +=1
    rover_id=rover_id_count
    rovers_dict[rover_id] =RoverSimulation.Rover(rover_id,commands,copy.deepcopy(rover_map))
    return {"id": rover_id}

# To delete a rover with the “:id”
@app.delete("/rovers/{rover_id}")
def delete_rover(rover_id: int):
    global rovers_dict
    if rover_id not in rovers_dict:
        raise HTTPException(status_code=404, detail="Rover not found")
    del rovers_dict[rover_id]
    return {"message": "Rover deleted successfully"}

# To send the list of commands to a rover as a String. Note if
# the rover status is not “Not Started” nor “Finished”, a failure
# response should be returned
@app.put("/rovers/{rover_id}")
def update_rover_commands(rover_id: int, commands: str):
    global rovers_dict
    if rover_id not in rovers_dict:
        raise HTTPException(status_code=404, detail="Rover not found")
    rover =rovers_dict[rover_id]
    if rover.status not in ["Not Started", "Finished"]:
        raise HTTPException(status_code=400, detail="Cannot update commands for a running rover")
    if not check_commands(commands):
        raise HTTPException(status_code=400, detail="Commands invalid")
    rover.moves = commands
    return {"message":"Rover commands successfully updated"}

# To dispatch a rover with the “:id”, the response should
# include the ID, status, latest position and list of the executed
# commands of the rover.
@app.post("/rovers/{rover_id}/dispatch")
def dispatch_rover(rover_id: int):
    global rovers_dict
    if rover_id not in rovers_dict:
        raise HTTPException(status_code=404, detail="Rover not found")
    rover = rovers_dict[rover_id]
    if rover.status == "Not Started":
        pos_mine_dic = convert_mine_dic()
        rover.move3(pos_mine_dic)
    rover_info = {
        "id": rover_id,
        "status": rover.status,
        "position": str(rover.x) + "," + str(rover.y),
        "executed_commands": rover.executed_commands,
        "map": rover.map
    }
    rover.update_map()
    return json.dumps(rover_info, indent=4)


# WebSocket Endpoint
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#     except WebSocketDisconnect:
#         print("Client disconnected")
