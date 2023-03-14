#sing MQTT to report the connection status of a LoRa gateway:


import time
import paho.mqtt.client as mqtt

# Define the MQTT broker connection parameters
mqtt_broker_url = 'mqtt://example.com'
mqtt_broker_port = 1883
mqtt_topic = 'lora_gateway/network_status'

# Define the retry interval in seconds
retry_interval = 5

# Initialize the MQTT client
client = mqtt.Client()

# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
        # Publish the initial connection status
        publish_network_status('connected')
    else:
        print('Connection to MQTT broker failed')

def on_disconnect(client, userdata, rc):
    print('Disconnected from MQTT broker')
    # Publish the disconnection status and the time of disconnection
    publish_network_status('disconnected', time.time())

# Connect to the MQTT broker and set the callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(mqtt_broker_url, mqtt_broker_port)

# Define the function to publish the network status
def publish_network_status(status, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    payload = {'status': status, 'timestamp': timestamp}
    client.publish(mqtt_topic, payload)

# Start the MQTT client loop
client.loop_start()

# Record the number of retries
num_retries = 0

while True:
    # Check if the client is connected to the broker
    if not client.is_connected():
        # Record the time of disconnection
        time_disconnected = int(time.time())
        # Wait for the retry interval before reconnecting
        time.sleep(retry_interval)
        # Try to reconnect to the broker
        try:
            client.reconnect()
            num_retries += 1
        except:
            pass
    else:
        # Publish the reconnection status and the time of reconnection
        publish_network_status('connected', time.time())
        # Reset the number of retries
        num_retries = 0
    # Wait for 1 second before checking the connection again
    time.sleep(1)
