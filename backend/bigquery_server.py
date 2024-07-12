from flask import Flask, jsonify
from google.cloud import bigquery
import os
import json
import configparser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Set the path to your Google Cloud credentials
# Create a ConfigParser object
config = configparser.ConfigParser(interpolation=None)

# Read the settings file
config.read('settings.ini')

credentials_path = config['DEFAULT']['credentials_path']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# Initialize a BigQuery client
client = bigquery.Client()

@app.route('/api/data', methods=['GET'])
def get_data():
    query = """
    SELECT *
    FROM `helical-bonsai-428613-q5.ArrowPointRealTime.pubsubprice`
    ORDER BY SAFE_CAST(JSON_EXTRACT(data, '$.timestamp') AS FLOAT64)
    """
    query_job = client.query(query)
    results = query_job.result()

    data = []
    for row in results:
        row_dict = dict(row)
        if 'data' in row_dict:
            try:
                nested_data = json.loads(row_dict['data'])
                nested_data['timestamp'] = float(nested_data['timestamp'])
                data.append(nested_data)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error processing row: {e}")
                continue

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)