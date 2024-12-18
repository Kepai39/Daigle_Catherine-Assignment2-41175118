from azure.iot.device.aio import IoTHubDeviceClient
from dotenv import load_dotenv

# imports
import random
import datetime
import time
import json
import asyncio
import os

# Sourced/Adapted from Avirup Basu, available on GitHub: https://github.com/avirup171/python-iot-hub-sender
# Define connection strings, loading from environment into array 'connectionStrings'
load_dotenv()
connectionStrings = [os.getenv('IOTHUB_CONN_STR1'), os.getenv('IOTHUB_CONN_STR2'), os.getenv('IOTHUB_CONN_STR3')]
print("Connection Strings:\n" + connectionStrings[0] + ", \n" + connectionStrings[1] + ", \n" + connectionStrings[2])

async def sendToIotHub(data, conn):
    try:
        # Create an instance of the IoT Hub Client class, passing the connection string using the index (conn)
        deviceId = IoTHubDeviceClient.create_from_connection_string(connectionStrings[conn])

        # Connect the device client
        await deviceId.connect()

        #Send the message
        await deviceId.send_message(data)
        print("Message sent to IoT Hub:", data)

        # Shutdown the client
        await deviceId.shutdown()
        
    
    except Exception as e:
        print("Error:", str(e))

def main():
    # Run an infinite while loop to send data every 5 seconds
    while True:
        # Generate random value
        locations = ["Dow's Lake", "Fifth Avenue", "NAC"]

        # Generate data packet
        # Inner loop. Enumerate makes a tuple of locations in x, with x[0] giving the index of this inner loop
        for x in enumerate(locations):
            iceThickness = random.randrange(0, 10) # generates a random num between 0 and 10
            surfaceTemp = random.randrange(-30, 10) # generates a random num between -30 and 10 for temp
            snowAccumulation = random.randrange(0, 10) # generates a random num between 0 and 10
            externalTemp = random.randrange(-30, 10) # generates a random number between -30 and 10
            
            msgData={ # pass the generated variables to an object
                "location": locations[x[0]],
                "iceThickness": iceThickness,
                "surfaceTemperature": surfaceTemp,
                "snowAccumulation": snowAccumulation,
                "externalTemperature": externalTemp,
                "timestamp":str(datetime.datetime.now())
            }
            # the following runs an asynchronous task, sendToIotHub(), passing our payload 'msgData' and the index 'x[0]'
            asyncio.run(sendToIotHub(data=json.dumps(msgData), conn=x[0]))
            time.sleep(10)

if __name__ == '__main__':
    main()