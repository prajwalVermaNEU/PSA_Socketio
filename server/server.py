from urllib.parse import parse_qs
from fastapi import FastAPI
import socketio
import uvicorn
import random
from collections import defaultdict

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()

# Mount Socket.IO to FastAPI
app.mount("/", socketio.ASGIApp(sio, app))

# connections
connected_clients, match_count = {}, 0
active_students = defaultdict( list )
def create_room():
    return "ROOM_" + str(random.randint( 100, 999))

async def join_room(sid, room_name):
    await sio.enter_room(sid, room_name)
    print(f"Student {sid} joined room: {room_name}")

WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
def create_apple():
    apple_posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) // SEG_SIZE)
    apple_posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) // SEG_SIZE)
    return (apple_posx, apple_posy)

async def create_match( currLevel):
    if len( active_students[currLevel]) > 1:
        # pop the last two elements and then add them into a room, notify them and finaly start the match ...
        player_1 = active_students[currLevel].pop()
        player_2 = active_students[currLevel].pop()

        currRoom = create_room()
        await join_room( player_1, currRoom)
        await join_room( player_2, currRoom)

        # Notify both players about each other
        await sio.emit("MATCH_STARTED", {
            "room": currRoom,
            "player_1": player_1,
            "player_2": player_2,
            "APPLE_POS": create_apple()
        }, room=currRoom)
    else:
        await sio.emit( "response", "SERVER: Kindly wait for sometime, we will find a pair for you to play")

@sio.event
async def update_snake_position( sid, data):
    room, position = data["room"], data["position"]
    print("Sending the coors from:", sid, " of :", position)
    await sio.emit("opponent_snake_position", {
        "player":sid,
        "position": position
    }, room = room, skip_sid=sid)

def getTheWiner( room, loser):
    print(":Here I need to cone")


@sio.event
async def game_over( sid, data):
    room = data["room"]
    loser = data["loser"]

    print("Game Over!")
    await sio.event("game_result",{
        "room":room,
    }, room = room, skip_sid=sid)
    winner = getTheWiner(room, loser)
    await sio.leave_room(loser, room)
    await sio.leave_room(winner, room)

@sio.event
async def connect(sid, env, *args):
    print(f"Student: {sid} connected")
    query_string = env.get("QUERY_STRING", "")
    query_params = parse_qs(query_string)
    NU_ID = query_params.get("NU_ID", ["XXXXXXXXX"])[0]
    MAIL_ID = query_params.get("MAIL_ID", ["guest@northeastern.com"])[0]
    connected_clients[sid] = {
        "NU_ID":NU_ID,
        "MAIL_ID":MAIL_ID,
    }
    # await sio.emit("USER-CONNECTED", {"sid": sid}, to=None, skip_sid=sid)
    active_students[0].append( sid )
    await create_match(0)


@sio.event
async def disconnect(sid):
    print(f"Student: {sid} disconnected")
    connected_clients.pop(sid,None)
    # await sio.emit("USER-DISCONNECTED", {"sid": sid}, to=None, skip_sid=sid)

@sio.event
async def leave_room(sid, room_name):
    await sio.leave_room(sid, room_name)
    print(f"Client {sid} left room: {room_name}")
    # await sio.emit("room_message", {"message": f"{sid} left {room_name}"}, room=room_name)


@sio.event
async def response(sid, data):
    print(f"Got a msg from {sid} {data}")
    # 1. Have the follow up match if possible and also notify the user to wait till the time comes
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




# Here are the things required to complete:

# 1, notify the opponent that the game is over and then looser will be out of game and the winner till continue
# 2. maintin the points to each of the winners
# 3. finally when the match is over how to migrate it to the next match and thus if looser if there then close this thread
# 4. for the winner we will continue
# 5. finally close the tounament.
# 6. Next phase we need to work over the UI where we can display the result.


