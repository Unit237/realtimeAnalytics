import eventlet
from flask import Flask
from flask_socketio import SocketIO
import os
import json
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
import threading
import time
import configparser

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

# Set Google Cloud credentials environment variable
# Create a ConfigParser object
config = configparser.ConfigParser(interpolation=None)

# Read the settings file
config.read('settings.ini')

credentials_path = config['DEFAULT']['credentials_path']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Initialize Pub/Sub client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/helical-bonsai-428613-q5/subscriptions/real-time-price-sub'

# Global variable to track events
tick = 0
value = '12'
# Define callback function to handle Pub/Sub messages
def callback(message):
    global tick
    global value
    print(f"Received message: {message}")
    
    # Process message data
    try:
        message_data = json.loads(message.data.decode('utf-8'))
        value = message_data.get('price')
        tick += 1
    except json.JSONDecodeError as e:
        print(f"Error decoding message data: {e}")

    # Acknowledge the message
    message.ack()

# SocketIO event handler for client connection
@socketio.on('connect')
def handle_connect():
    print('Client connected', value)
    stream_thread = threading.Thread(target=emit_stream)
    stream_thread.start()
    

def emit_stream():
    global value, tick, socketio
    prev_value = value
    while True:
        socketio.sleep(1)
        if prev_value != value:
            socketio.emit('cpu', {'name': tick, 'value': value})
            print(f"Emitting 'cpu' event: name={tick}, value={value}")
            prev_value = value

# Function to run SocketIO server
def run_socketio():
    socketio.run(app, host='localhost', port=3007)

if __name__ == '__main__':
    # Start SocketIO server in a separate thread
    socketio_thread = threading.Thread(target=run_socketio)
    # Subscribe to Pub/Sub subscription and start listening for messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}")
    socketio_thread.start()
    #eventlet.spawn(emit_stream)

    # Keep the main thread from exiting so the subscriber can continue to receive messages
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    # Run the Flask application in the main thread
    app.run()
