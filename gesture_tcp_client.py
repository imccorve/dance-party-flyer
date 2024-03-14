import socket
import json
import numpy as np
from pythonosc import udp_client

tidal_host = "127.0.0.1"
tidal_port = 6010

tidal_osc_client = udp_client.SimpleUDPClient(tidal_host, tidal_port)

# Need this for the OSC connection with SuperCollider
def send_osc_message(gesture):
    client = udp_client.SimpleUDPClient("127.0.0.1", 12345)
    client.send_message("/gesture", gesture)

def send_gesture_data(gesture):
    # Convert numpy int64 to native Python int if necessary
    if isinstance(gesture, np.integer):
        gesture = int(gesture)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 12345))  # Replace with server's IP address and port
        data = json.dumps({"gesture": gesture})
        s.sendall(data.encode('utf-8'))
        
        send_osc_message(data)
        tidal_osc_client.send_message("/ctrl",["amp", 5])
        tidal_osc_client.send_message("/ctrl", ["speed", 5])



# # Example usage
# while True:
#     frame = get_video_frame()  # Your method to capture video frames
#     gesture = recognize_gesture(frame)
#     if gesture:
#         send_gesture_data(gesture)
