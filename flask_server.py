from flask import Flask, request, jsonify
import requests
import json
import serial
import time

app = Flask(__name__)

# Define the Arduino serial port and baud rate
arduino_port = '/dev/ttyUSB0'  # Update with your Arduino port
baud_rate = 9600

# Variable to store received md5 value
received_md5 = None

@app.route('/receive_md5', methods=['POST'])
def receive_md5():
    global received_md5
    
    data = request.get_json()
    md5 = data['md5']
    
    # Store the received md5 value
    received_md5 = md5
    
    print(f"Received MD5: {received_md5}")  # Print or use the md5 value as needed
    
    url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5"

    payload = json.dumps({
        "md5": md5
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN_HERE'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # Parse the JSON response
    parsed_response = response.json()

    # Extract the "amount" value
    amount = parsed_response["data"]["amount"]

    # Open serial connection to Arduino
    arduino = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for the Arduino to initialize

    # Send the amount data to Arduino
    arduino.write(str(amount).encode())

    # Close serial connection
    arduino.close()

    return jsonify({'status': 'success', 'amount': amount})

# Route to get the current md5 value
@app.route('/get_md5', methods=['GET'])
def get_md5():
    global received_md5
    
    if received_md5 is None:
        return jsonify({'error': 'No md5 value received yet'})
    else:
        return jsonify({'md5': received_md5})

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Use a different port, e.g., 5001
