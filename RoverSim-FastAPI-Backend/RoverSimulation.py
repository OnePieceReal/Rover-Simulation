import requests
import time
import threading
import hashlib
import itertools
import random
import copy
import multiprocessing
import os
# import myproto_pb2
# import myproto_pb2_grpc

#final 2
TOTAL_ROVERS = 10
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MINE_TXT_FILE_LOCATION = os.path.join(BASE_DIR, "mines.txt")
MAP_TXT_FILE_LOCATION = os.path.join(BASE_DIR, "map.txt")

def create_map():
    # opening a file in python
    with open(MAP_TXT_FILE_LOCATION , 'r') as file:
        content = file.read()
    rows,columns = int(content[0]),int(content[2])
    #initialize 2d array
    map = [[' ' for _ in range(columns)] for _ in range(rows)]
    k = 3
    for i in range(rows):
        for j in range(columns):
            while content[k] == '\n' or content[k] == ' ':
                k+=1
            map[i][j] = content[k]
            k+=1
    #print(map)
    return map

def load_mine_data():
    with open(MINE_TXT_FILE_LOCATION , 'r') as file:
        mine_serial_numbers = [line.strip() for line in file]
    map_data = create_map()
    pos_mine_dic= {}
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j].isdigit() and int(map_data[i][j]) > 0:
                mine_serial = mine_serial_numbers[ random.randint(0,len(mine_serial_numbers))% (len(mine_serial_numbers)-1)]
                assigned_pin = mine_serial
                pos_mine_dic[(i, j)] = assigned_pin
    #print(pos_mine_dic)
    return  pos_mine_dic

def try_pin(pin, serial_number):
    mine_key = pin + serial_number
    # Hash the mine key using SHA-256
    hash_value = hashlib.sha256(mine_key.encode()).hexdigest()
    # Check if the hash has at least 6 leading zeros
    if hash_value.startswith("000000"):
        return mine_key  # Return the valid mine key (PIN + serial number)
    return None

def find_valid_pin(rover_id,serial_number, pin_length=6):
    initial_ser_num =serial_number
    start_time = time.time()
    # Define the characters to be used in the PIN (digits, letters, and special characters)
    char_set = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
    rand_num=random.randint(0,100)
    serial_number = str( rand_num) +serial_number #start with an arbitrary string
    # Generate all possible combinations of the specified length
    for pin_tuple in itertools.product(char_set, repeat=pin_length):
        pin = ''.join(pin_tuple)
        result = try_pin(pin, serial_number)
        if result:
            print(f"Rover {rover_id} disarmed mine with key: {result}")
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Rover {rover_id} time taken to disarm mine: {time_taken:.2f} seconds")
            return (pin+str(rand_num)), time_taken, result
    return None

DIRECTIONS = {
    0: (-1, 0),  #  (North)
    1: (0, 1),   #  (East)
    2: (1, 0),   #  (South)
    3: (0, -1)   #  (West)
}

# Maps index -> Direction Name
INDEX_TO_DIRECTION = {
    0: 'N',
    1: 'E',
    2: 'S',
    3: 'W'
}

class Rover:
    current_direction = 2 #rover initially facing south
    x = 0
    y = 0
    is_alive = True
    mine_disarm_info = "\nMine Disarm info:\n"
    TTTDM = 0 #total time taken to disarm mine(s)
    pin =""
    status="Not Started"
    executed_commands=""
    map_update_status=False

    def __init__(self,id,moves,map):
        self.id = id
        self.moves=moves
        self.map =copy.deepcopy(map)
        self.backup_map = copy.deepcopy(map)
    def __str__(self):
        return f"ID: {self.id} Moves:" +self.moves

    def move(self, enableMineSimulation = False, enableTextFileUpdate = True ):

        # Command    | Meaning
        # ---------------------
        # L          | Turn left
        # R          | Turn right
        # M          | Move forward
        # D          | Dig

        isMineActive = False
        pos_mine_dic = load_mine_data()  # assigns a serial number to each of mine found within the map
        for move in self.moves:
            # convert index to direction
            dx,dy = DIRECTIONS[self.current_direction]

            if self.check_mine():
               isMineActive = True

            if move == 'M' and (not isMineActive):
                self.map[self.x][self.y] = '*' #ensures that the initial position of the robot is marked
                #make sure the robot moves are within the map constraints
                if  self.x + dx < len(self.map) and  self.x + dx >= 0 and  self.y + dy < len(self.map[0]) and  self.y + dy >= 0:
                    #update the current position of the robot
                    self.x += dx
                    self.y += dy
                    if not (self.check_mine()):
                        self.map[self.x][self.y] = '*'

            elif move  == 'D' :
                if self.check_mine():
                    if enableMineSimulation:
                        if not (self.disarm_mine(pos_mine_dic[(self.x, self.y)])):
                                self.is_alive= False
                                break
                    self.map[self.x][self.y] = '*'
                    isMineActive = False

            elif move == 'R' :
                 if self.current_direction + 1 > 3:
                    self.current_direction=0
                 else:
                     self.current_direction+=1
            elif move == 'L' :
                if self.current_direction -1 < 0:
                    self.current_direction = 3
                else:
                    self.current_direction -= 1
            else:
                self.is_alive = False
                break
        if enableTextFileUpdate:
            self.update_txt_file()
        print("Rover "+str(self.id)+" has completed execution!")

    # def move2(self, pos_mine_dic,channel):
    #     stub = myproto_pb2_grpc.GroundControlStub(channel)
    #
    #     isMineActive = False
    #     for move in self.moves:
    #         # convert index to direction
    #         dx, dy = DIRECTIONS[self.current_direction]
    #
    #         if self.check_mine():
    #             isMineActive = True
    #
    #         if move == 'M' and (not isMineActive):
    #             self.map[self.x][self.y] = '*'  # ensures that the initial position of the robot is marked
    #             # make sure the robot moves are within the map constraints
    #             if self.x + dx < len(self.map) and self.x + dx >= 0 and self.y + dy < len(
    #                     self.map[0]) and self.y + dy >= 0:
    #                 # update the current position of the robot
    #                 self.x += dx
    #                 self.y += dy
    #                 if not (self.check_mine()):
    #                     self.map[self.x][self.y] = '*'
    #
    #         elif move == 'D':
    #             if self.check_mine():
    #                 if True:
    #                     if not (self.disarm_mine(pos_mine_dic[(self.x, self.y)])):
    #                         self.is_alive = False
    #                         break
    #                 self.map[self.x][self.y] = '*'
    #                 pos ="("+str(self.x)+","+str(self.y)+")"
    #                 mine_pin_request = myproto_pb2.MinePinRequest(rover_id=self.id, pin=self.pin,position=pos)
    #                 mine_pin_response = stub.ShareMinePin(mine_pin_request)
    #                 print(f"PIN send response status: {mine_pin_response.received}")
    #                 isMineActive = False
    #         elif move == 'R':
    #             if self.current_direction + 1 > 3:
    #                 self.current_direction = 0
    #             else:
    #                 self.current_direction += 1
    #         elif move == 'L':
    #             if self.current_direction - 1 < 0:
    #                 self.current_direction = 3
    #             else:
    #                 self.current_direction -= 1
    #         else:
    #             self.is_alive = False
    #             break
    #     if True:
    #         self.update_txt_file()
    #     #print("Rover " + str(self.id) + " has completed execution!")

    def move3(self, pos_mine_dic):
        self.status="Moving"
        isMineActive = False
        for move in self.moves:
            self.executed_commands += move
            # convert index to direction
            dx, dy = DIRECTIONS[self.current_direction]

            if self.check_mine():
                isMineActive = True

            if move == 'M' and (not isMineActive):
                self.map[self.x][self.y] = '*'  # ensures that the initial position of the robot is marked
                # make sure the robot moves are within the map constraints
                if self.x + dx < len(self.map) and self.x + dx >= 0 and self.y + dy < len(
                        self.map[0]) and self.y + dy >= 0:
                    # update the current position of the robot
                    self.x += dx
                    self.y += dy
                    if not (self.check_mine()):
                        self.map[self.x][self.y] = '*'

            elif move == 'D':
                if self.check_mine():
                    if True:
                        if not (self.disarm_mine(pos_mine_dic[(self.x, self.y)])):
                            self.status="Eliminated"
                            self.is_alive = False
                            break
                    self.map[self.x][self.y] = '*'
                    isMineActive = False
            elif move == 'R':
                if self.current_direction + 1 > 3:
                    self.current_direction = 0
                else:
                    self.current_direction += 1
            elif move == 'L':
                if self.current_direction - 1 < 0:
                    self.current_direction = 3
                else:
                    self.current_direction -= 1
            else:
                self.is_alive = False
                self.status = "Eliminated"
                break

        # if False:
        #     self.update_txt_file()
        if self.status != "Eliminated":
            self.status = "Finished"
        # if self.map_update_status:
        #     placeholder_map =self.map
        #     self.map = self.backup_map
        #     self.backup_map=placeholder_map

    def disarm_mine(self,serial_number):
        result = find_valid_pin(self.id,serial_number)
        if(result != None):#lmao
            self.mine_disarm_info += "Mine serial number: ["+serial_number+"]\n"+"Disarmed at position ("+str(self.x)+","+str(self.y)+") with the pin: ["+result[0]+"]\n" +"Time taken to disarm: "+str(result[1])+" sec\n"+"Hash Value: "+result[2]+"\n"
            self.TTTDM += result[1]
            self.pin=result[0]
            return True
        self.mine_disarm_info += "\nUnable to disarm mine at position ("+str(self.x)+","+str(self.y)+")"
        return False

    def update_txt_file(self):
         file_name = "Rover"+str(self.id)+"Map"
         content = "Rover ID: "+str(self.id)+"\n"
         content += "Rover Moves:" +self.moves+"\n"
         content += "Rover Path: "+"\n"
         with open(file_name, 'w') as file:
             for i in range(len(self.map)):
                 for j in range(len(self.map[0])):
                     content +=self.map[i][j]
                     content += " "
                     if j == len(self.map[0]) -1:
                         content +=  "\n"
             content += "Rover Alive? "+str(self.is_alive)+"\n"
             content += self.mine_disarm_info
             file.write(content)

    def check_mine(self):
        if self.map[self.x][self.y] != '*' and int(self.map[self.x][self.y]) > 0:
            return True
        return False

    def update_map(self):
        if self.map_update_status:
            self.map = copy.deepcopy(self.backup_map)
            self.reset()
            self.map_update_status = False

    def reset(self):
        self.current_direction = 2  # rover initially facing south
        self.x = 0
        self.y = 0
        self.is_alive = True
        self.mine_disarm_info = "\nMine Disarm info:\n"
        self.TTTDM = 0  # total time taken to disarm mine(s)
        self.pin = ""
        self.status = "Not Started"
        self.executed_commands = ""
        self.map_update_status = False


def initialize_rovers():
    url = "https://coe892.reev.dev/lab1/rover/"
    rovers = []
    map = create_map()
    for i in range (TOTAL_ROVERS):
        try:
            response = requests.get(url+str(i+1))
            response.raise_for_status()
            json_data = response.json()
            moves = json_data['data']['moves']
            rovers.append(Rover(i+1,moves,copy.deepcopy(map)))
        except requests.exceptions.RequestException as e:
            print(f"An error has occurred: {e}")
    return rovers

def sequential_approach(enableMineDigSimulation = False):
    start_time = time.time()
    rovers = initialize_rovers()
    total_disarm_time = 0
    for rover in rovers:
        if enableMineDigSimulation:
            rover.move(True)
            total_disarm_time += rover.TTTDM
        else:
            rover.move()
    end_time = time.time()
    execution_time = end_time - start_time
    if enableMineDigSimulation:
        print("\nSequential Approach - total time taken to disarm mine(s): "+str(total_disarm_time))
        return total_disarm_time
    else:
        print(f"Sequential approach execution time: {execution_time:.6f} seconds")

    return execution_time

def run_rover(rover,enableMineDigSimulation = False):
    if(enableMineDigSimulation):
        rover.move(True)
    else:
        rover.move()

def parallel_thread_approach(enableMineDigSimulation = False):
    start_time = time.time()
    rovers = initialize_rovers()
    threads = []
    for rover in rovers:
        if enableMineDigSimulation:
            thread = threading.Thread(target=run_rover, args=(rover,True,))
        else:
            thread = threading.Thread(target=run_rover, args=(rover,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    execution_time = end_time - start_time


    if enableMineDigSimulation:
        total_disarm_time = 0
        for rover in rovers:
            total_disarm_time +=rover.TTTDM
        print(f"\nMultithreaded approach  - total time taken to disarm mine: {total_disarm_time :.6f} seconds")
        return  total_disarm_time
    else:
        print(f"Multithreaded approach execution time: {execution_time:.6f} seconds")
    return execution_time

def execute_rovers_parallel(enableMineDigSimulation=False):
    start_time = time.time()
    rovers = initialize_rovers()
    processes = []

    for rover in rovers:
        if enableMineDigSimulation:
            process = multiprocessing.Process(target=run_rover, args=(rover, True,))
        else:
            process = multiprocessing.Process(target=run_rover, args=(rover,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Parallel approach execution time: {execution_time:.6f} seconds")

    if enableMineDigSimulation:
        total_disarm_time = sum(rover.TTTDM for rover in rovers)
        print(f"\nParallel approach - total time taken to disarm mine: {total_disarm_time:.6f} seconds")

def main():
    """Part 1: Drawing the path of the rovers"""
    # Run the sequential approach
    print("Running sequential approach...[Loop]")
    computation_time_seq_approach = sequential_approach()

    #use python threading module
    print("Running parallel approach... [Threads]")
    computation_time_thread_approach = parallel_thread_approach()

    # calculate difference in computation time
    print("Calculating Difference in computation time... [sequential approach] vs. [Threads]")
    difference_approach = abs(computation_time_seq_approach-computation_time_thread_approach)
    print("abs[(Parallel ET)- (Sequential ET)]: "+str(difference_approach )+" seconds")

    """Part 2: Digging mines"""
    # # Run the sequential approach w/ dig/disarm simulation
    print("\nRunning sequential approach w/ dig/disarm simulation...")
    mine_simualtion_etime_seq= sequential_approach(True)
    # Using python threading module approach w/ dig/disarm simulation

    print("\nMultithreaded approach w/ dig/disarm simulation...")
    mine_simualtion_etime_thread=parallel_thread_approach(True)

    # calculate difference in computation time
    print("Calculating Difference in computation time w/dig/diarm simulation enabled... [sequential approach] vs. [Threads]")
    difference_approach_w_disarmsim = abs(mine_simualtion_etime_thread-mine_simualtion_etime_seq)
    print("abs[(Parallel ET)- (Sequential ET)]: "+str(difference_approach_w_disarmsim)+" seconds")

if __name__ == "__main__":
    main()












