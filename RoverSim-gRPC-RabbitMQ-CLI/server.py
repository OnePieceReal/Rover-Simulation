import grpc
from concurrent import futures
import time
import myproto_pb2
import myproto_pb2_grpc
import RoverSimulation
import random
import pika

#final 3
rovers = RoverSimulation.initialize_rovers()

def map_to_string(map):
    content = str(len(map))+" "+str(len(map[0]))+"\n"
    for i in range(len(map)):
        for j in range(len(map[0])):
            content += map[i][j]
            content += " "
            if j == len(map[0]) - 1:
                content += "\n"
    return content

def get_random_serial_number():
    with open(RoverSimulation.MINE_TXT_FILE_LOCATION, 'r') as file:
        mine_serial_numbers = [line.strip() for line in file]
    return mine_serial_numbers[ random.randint(0,len(mine_serial_numbers))% (len(mine_serial_numbers)-1)]

class GroundControlServicer(myproto_pb2_grpc.GroundControlServicer):
    #returns map based on rover id -- completed
    def GetMap(self, request, context):
        rover_id = request.rover_id-1
        rover_map = (rovers[rover_id]).map
        string_map = map_to_string(rover_map)
        return myproto_pb2.MapResponse(map=string_map)

    #returns commands of the rover based on its id --completed
    def GetCommands(self, request, context):
        rover_id = request.rover_id - 1
        rover_commands = (rovers[rover_id]).moves
        return myproto_pb2.CommandResponse(commands=rover_commands)

    #returns a random serial number to the client --completed
    def GetMineSerialNumber(self, request, context):
        return myproto_pb2.MineSerialResponse(serial_number=get_random_serial_number())

def callback(ch, method, properties, body):
    #Callback function executed when message is received.
    print(f"Received message: {body.decode()}")

def subscribe_to_queue(queue_name):
    #Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #Declare the queue
    channel.queue_declare(queue=queue_name)
    #Subscribe to the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Subscribed to '{queue_name}'. Waiting for messages...")
    #Start consuming messages
    channel.start_consuming()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    myproto_pb2_grpc.add_GroundControlServicer_to_server(GroundControlServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running on port 50051...")
    subscribe_to_queue("Defused_Mines")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
