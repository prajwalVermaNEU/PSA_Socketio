import socketio

SERVER_IP = "172.16.46.123"
NU_ID = "002879993",
MAIL_ID = "verma.praj@northeastern.edu",

sio = socketio.Client()

@sio.event
def connect():
    print("Success, You are connected to CLASS_SERVER")

@sio.event
def disconnect():
    print("Disconnected from the CLASS_SERVER")

@sio.event
def response(data):
    print("Server response:", data)

sio.connect(f"http://{SERVER_IP}:8000?NU_ID={NU_ID}&MAIL_ID={MAIL_ID}")
# sio.connect(f"http://{SERVER_IP}:8000")
sio.wait()

# @sio.event
# def chat(data):
#     print(f"Client {data['sid']} says: {data['message']}")

# @sio.event
# def user_connected(data):
#     print(f"New client connected: {data['sid']}")

# @sio.event
# def user_disconnected(data):
#     print(f"Client {data['sid']} disconnected")



# Use the server's local IP instead of localhost


# Send a message
# sio.emit("message", {
# })

# Chat loop to send messages
# while True:
#     msg = input("You: ")
#     if msg.lower() == "exit":
#         sio.disconnect()
#         break
#     sio.emit("message", msg)

# # Keep the connection open
# sio.wait()

