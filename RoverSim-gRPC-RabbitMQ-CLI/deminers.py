
import pika
import sys

from RoverSimulation import find_valid_pin
##final 3
def process_mine(mine_data):
    # Assuming format: "id||x||y||serial_number"
    mine_data_list = mine_data.split("||")
    if len(mine_data_list) == 5:
        rover_id = int(mine_data_list[0])
        mine_id = int(mine_data_list[1])
        x= int(mine_data_list[2])
        y= int(mine_data_list[3])
        serial_number= mine_data_list[4]
        result = find_valid_pin(rover_id, serial_number )
        return result[0], mine_id, (x,y), rover_id,serial_number
    else:
        print("Error: Invalid mine data format.")
        return

def callback(ch, method, properties, body):
    mine_data = body.decode()
    print(f"Recieved the following mine data: {mine_data}")
    # disarm the mine first
    results = process_mine(mine_data)
    # Publish the PIN to the Defused_Mines queue
    message = f"Mine with id = {results[1]} and serial number {results[4]} disarmed at position {results[2]} with pin {results[0]}"
    publish_pin(results[0])
    # Send a response back to the client only if a reply_queue is specified
    if properties.reply_to:
        response = message
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=response,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id  # Use the same correlation_id
            )
        )
        #print(f"Sent response to client: {response}")
    # Acknowledge message to remove it from queue
    ch.basic_ack(delivery_tag=method.delivery_tag)

def publish_pin(pin):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Declare the Defused_Mines queue
    channel.queue_declare(queue='Defused_Mines')
    # Publish the PIN to the Defused-Mines queue
    channel.basic_publish(exchange='',
                          routing_key='Defused_Mines',
                          body=pin)
    print(f"Published PIN: {pin} ")
    connection.close()

def subscribe_to_queue(deminer_number):
    #Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #Declare the Demine_Queue
    channel.queue_declare(queue='Demine_Queue')
    print(f" Deminer {deminer_number} is waiting for mine data...")
    # Subscribe to the Demine_Queue
    channel.basic_consume(queue='Demine_Queue', on_message_callback=callback, auto_ack=False)
    # start consuming messages (blocking call)
    channel.start_consuming()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deminer.py <deminer_number>")
        sys.exit(1)
    #Validate that the deminer number.
    deminer_number = int(sys.argv[1])
    if deminer_number not in [1, 2]:
        print("Error: Deminer number must be 1 or 2.")
        sys.exit(1)
    deminer_number = int(sys.argv[1])
    subscribe_to_queue(deminer_number)
