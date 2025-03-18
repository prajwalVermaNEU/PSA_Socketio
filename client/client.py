import socketio
from game import createGame, update_opponent_data, getCurrSnake, main, insert_apple, game_over
import tkinter as tk  # Import tkinter in client.py
import threading 
import time

SERVER_IP = "172.16.46.123"
# SERVER_IP = "10.110.19.88"
NU_ID = "002879993"
MAIL_ID = "verma.praj@northeastern.edu"

sio = socketio.Client()
root = tk.Tk()
root.title("PSA INFO 6205 Snake game")

game_running = False

@sio.event
def connect():
    print("Success, You are connected to CLASS_SERVER")

@sio.event
def disconnect():
    print("Disconnected from the CLASS_SERVER")

@sio.event
def response(data):
    print("INFORMATION: ", data)

@sio.on("MATCH_STARTED")
def match_started(data):
    print("YOUR MATCH STARTED!")
    room = data["room"]
    global game_running
    game_running = True

    def start_game():
        global currSnake
        createGame(root, data['APPLE_POS'])
        root.after(100, play)

    def play():
        global game_running
        if not game_running:
            return
        
        currSnake = getCurrSnake()
        # print("Current Coordinates: ", currSnake.getAllCoords() )
        if currSnake is not None:
            sio.emit("update_snake_position", {"room": room, "position": currSnake.getAllCoords()})
        status = main()
        if status['STATUS'] == "GAME-OVER":
            sio.emit("game_over", {"room": room, "loser": sio.sid})
            return
        elif status['STATUS'] == "CREATE_APPLE":
            sio.emit("update_apple", {"room":room})
        root.after( 50, play)
    
    root.after(0, start_game)

@sio.on("update_apple")
def update_apple(data):
    print("Got new inputs for the apple ...", data)
    insert_apple( data['APPLE_POS'])

@sio.on("game_result")
def game_result(data):
    global game_running
    game_running = False
    winner, loser = data.get("winner", ""), data.get("loser", "")

    # This is the doubt I am having
    # print(sio.sid, winner, loser)

    
    if loser == sio.sid:
        print("😢 GAME OVER! You lost the match. Better luck next time.")
    else:
        print("🎉 CONGRATULATIONS! You won the match! 🎉")
    
    game_over()

@sio.on("opponent_snake_position")
def update_opponent_snake(data):
    """Update the opponent's snake position on our canvas."""
    position = data["position"]
    update_opponent_data(position)  

def connect_to_server():
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            print(f"🔗 Attempting to connect to {SERVER_IP}:8000... (Attempt {attempt + 1})")
            sio.connect(f"http://{SERVER_IP}:8000?NU_ID={NU_ID}&MAIL_ID={MAIL_ID}")
            print("✅ Connection Successful!")
            sio.wait()
            break
        except socketio.exceptions.ConnectionError as e:
            print(f"❌ Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("Maximum retry attempts reached. Exiting connection attempts.")

# Client connection:
socket_thread = threading.Thread(target=connect_to_server, daemon=True)
socket_thread.start()

root.mainloop()




# import socketio
# from game import createGame, update_opponent_data, getCurrSnake, main
# import tkinter as tk  # Import tkinter in client.py
# import threading 
# import time

# SERVER_IP = "172.16.46.123"
# NU_ID = "002879993"
# MAIL_ID = "verma.praj@northeastern.edu"

# sio = socketio.Client()
# root = tk.Tk()
# root.title("PSA INFO 6205 Snake game")

# @sio.event
# def connect():
#     print("Success, You are connected to CLASS_SERVER")

# @sio.event
# def disconnect():
#     print("Disconnected from the CLASS_SERVER")

# @sio.event
# def response(data):
#     print("INFORMATION: ", data)

# @sio.on("MATCH_STARTED")
# def match_started(data):
#     print("YOUR MATCH STARTED!")
#     room = data["room"]

#     def start_game():
#         global currSnake
#         createGame(root, data['APPLE_POS'])
#         root.after(100, play)

#     def play():
#         currSnake = getCurrSnake()
#         print("Current Coordinates: ", currSnake.getAllCoords() )
#         if currSnake is not None:
#             sio.emit("update_snake_position", {"room": room, "position": currSnake.getAllCoords()})
#         status = main()
#         if status['STATUS'] == "GAME-OVER":
#             print("SENT UPDATES TO SERVER. ")
#             print("You Lost!")

#             # update the server the game is over and current sid lost the match ... continue here ...
#             sio.emit("game_over", {"room": room, "loser": sio.sid})
#             return
#         root.after(100, play)
    
#     root.after(0, start_game)

# @sio.on("opponent_snake_position")
# def update_opponent_snake(data):
#     """Update the opponent's snake position on our canvas."""
#     position = data["position"]
#     update_opponent_data(position)  

# def connect_to_server():
#     max_retries = 5
#     retry_delay = 2

#     for attempt in range(max_retries):
#         try:
#             print(f"🔗 Attempting to connect to {SERVER_IP}:8000... (Attempt {attempt + 1})")
#             sio.connect(f"http://{SERVER_IP}:8000?NU_ID={NU_ID}&MAIL_ID={MAIL_ID}")
#             print("✅ Connection Successful!")
#             sio.wait()
#             break
#         except socketio.exceptions.ConnectionError as e:
#             print(f"❌ Connection attempt {attempt + 1} failed: {e}")
#             if attempt < max_retries - 1:
#                 print(f"Retrying in {retry_delay} seconds...")
#                 time.sleep(retry_delay)
#                 retry_delay *= 2
#             else:
#                 print("Maximum retry attempts reached. Exiting connection attempts.")

# # Client connection:
# socket_thread = threading.Thread(target=connect_to_server, daemon=True)
# socket_thread.start()

# root.mainloop()
