import grpc
import myproto_pb2
import myproto_pb2_grpc
import RoverSimulation
import argparse
import sys
import pika
import uuid

##final 3
def string_to_map(content):
    rows, columns = int(content[0]), int(content[2])
    # initialize 2d array
    map = [[' ' for _ in range(columns)] for _ in range(rows)]
    k = 3
    for i in range(rows):
        for j in range(columns):
            while content[k] == '\n' or content[k] == ' ':
                k += 1
            map[i][j] = content[k]
            k += 1
    #print(map)
    return map

def check_range(value):
    ivalue = int(value)  # Convert to integer
    if ivalue < 1 or ivalue > 10:
        raise argparse.ArgumentTypeError("The number must be between 1 and 10.")
    return ivalue

def publish_message_and_wait_for_reply(message, queue_name):
    # Establish connection
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Declare the requested queue
    channel.queue_declare(queue=queue_name)
    # Create a temporary reply queue to match response to original request
    result = channel.queue_declare(queue='', exclusive=True)
    reply_queue = result.method.queue
    correlation_id = str(uuid.uuid4())
    # Send the message with correlation_id and reply_to
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            reply_to=reply_queue,
            correlation_id=correlation_id,
            delivery_mode=2  # Make message persistent
        )
    )
    print(f"Message [{message}] published to {queue_name}. Waiting for response form reply queue '{reply_queue}'...")
    #simulates the disarm process, client has to wait for rover to disarm the mine
    #and can only proceed after it has published the information regarding the disarmed mine
    response = None
    def callback(ch, method, properties, body):
        nonlocal response
        if properties.correlation_id == correlation_id:
            response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()
    # Start consuming from the reply queue
    channel.basic_consume(queue=reply_queue, on_message_callback=callback)
    # Block and wait for the response
    channel.start_consuming()
    # Close the connection
    connection.close()
    print(f"Received Response from the deminer: {response}")
    print(f"Continuing rover execution....")
    return str(response)

class Mine:
    #mine id, coordinates, serial number
    def __init__(self, id,x,y, serial_number):
        self.id = id
        self.x=x
        self.y=y
        self.serial_number = serial_number
    def mine_message(self,rover_id):
        delim = "||"
        return f"{rover_id}{delim}{self.id}{delim}{self.x}{delim}{self.y}{delim}{self.serial_number}"

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = myproto_pb2_grpc.GroundControlStub(channel)

    parser = argparse.ArgumentParser(description="Only accepts integer between 1 and 10.")
    parser.add_argument("rover_id", type=check_range, help="Rover ID (1-10)")
    args = parser.parse_args()
    rover_id = args.rover_id

    #Request the map
    map_response = stub.GetMap(myproto_pb2.RoverRequest(rover_id=rover_id))
    print("Get map:\n"+map_response.map)
    map_data=string_to_map(map_response.map)

    # Request the commands
    commands_response = stub.GetCommands(myproto_pb2.RoverRequest(rover_id=rover_id))
    print(f"Get Rover {rover_id} commands: \n"+commands_response.commands+"\n")
    rover_commands = commands_response.commands

    # Request mine serial number for each mine on the map + create a dictionary
    mines= []
    mine_id=0
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j].isdigit() and int(map_data[i][j]) > 0:
                mine_serial_response = stub.GetMineSerialNumber(myproto_pb2.RoverRequest(rover_id=rover_id))
                print("Get mine serial number for mine at position: ("+str(i)+","+str(j)+"):\n"+mine_serial_response.serial_number)
                mine_serial_number = mine_serial_response.serial_number
                mine_id+=1
                mines.append(Mine(mine_id,i,j,mine_serial_number))

    #create a new rover class based on the above data
    print("\n")
    new_rover = RoverSimulation.Rover(rover_id,rover_commands,map_data)
    new_rover.move2(mines)

if __name__ == '__main__':
    run()
