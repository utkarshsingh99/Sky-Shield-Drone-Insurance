from flask import Flask, jsonify
import threading
import time
import pandas as pd
import csv
from flask_cors import CORS

# Create the Flask application
app = Flask(__name__)

obstacle_avoidance_mapping = {
   "Skydio 2": 0,
   "Parrot Anafi USA": 1,
   "DJI Mini 2": 1,
   "DJI Air 2S": 0,
   "Autel EVO Lite+": 0,
   "Skydio X2": 0,
   "Autel EVO Nano+": 0,
   "DJI Mavic Air 2": 0,
   "Yuneec Typhoon H": 0,
   "Autel EVO 2 Pro": 0
}


sheet_id = '1eIKOBrO7HKsQZs2Tu_Aw2Io4xO5aFMYkHjXoN5NtSos'
df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

# Enable CORS for all routes
CORS(app)

def load_data():
    while True:
        df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')
        last_entry = df.iloc[-1].to_list()

        data = {
            'Submitted On': last_entry[0],
            'Name': last_entry[1],
            'Drone': last_entry[2],
            'Email': last_entry[3],
            'Purchase Date': last_entry[4],
            'Coverage_Requested': last_entry[5],
            'Intended Use': last_entry[6],
            'Credit_Score': last_entry[7] if not pd.isna(last_entry[7]) else None,
            'Flying Certificate': last_entry[8],
            'Warranty': int(last_entry[9].split(' ')[0]) if last_entry[9].split(' ')[0] != 'No' else 0,
            # 'Services': last_entry[4],
            # 'Budget': last_entry[5],
            # 'How did you hear': last_entry[6],
            # 'Message': last_entry[7],
            # 'Risk Factor': last_entry[13]
        }
        obstacle_avoidance_factor = obstacle_avoidance_mapping[data['Drone']]
        # print(data['Warranty'])
        risk_factor = - 0.02*data['Warranty']- 0.01*obstacle_avoidance_factor + 0.76
        # You can put your logic here
        data['risk_factor'] = risk_factor
        if not all_requests or data['Submitted On'] != all_requests[-1]['Submitted On']:
            all_requests.append(data)
        time.sleep(1)



# Starting the function in a separate thread
thread = threading.Thread(target=load_data)
thread.daemon = True
thread.start()

all_requests = []

# Define a route and its associated view
@app.route('/')
def index():
    return 'This is the Flask API for data processing'

# Route for handling GET requests
@app.route('/api/data', methods=['GET'])
def get_data():
    return all_requests


# Run the Flask application
if __name__ == '__main__':
    app.run(port=8000, debug=True)