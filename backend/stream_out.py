import os
from google.cloud import pubsub_v1
import random
import time
from datetime import datetime
import json
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser(interpolation=None)

# Read the settings file
config.read('settings.ini')

credentials_path = config['DEFAULT']['credentials_path']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = config['DEFAULT']['topic_path']

for _ in range(7):
    random_float = round(random.uniform(1, 100), 2)
    random_float = str(random_float)

    data_message = 'new price value'
    data_message = data_message.encode('utf-8')
    datetime_int = int(datetime.now().replace(microsecond=0).timestamp())
    data = {
        'price': random_float,
        'timestamp': datetime_int
    }
    data = json.dumps(data)
    time.sleep(1)
    future = publisher.publish(topic_path, data=data.encode('utf-8'))
    print(f'published message id {future.result()}')
