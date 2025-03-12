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
def create_room():
    return "ROOM_" + str(random.randint( 100, 999))

@sio.event
async def join_room(sid, room_name):
    await sio.enter_room(sid, room_name)
    print(f"Client {sid} joined room: {room_name}")
    # await sio.emit("room_message", {"message": f"{sid} joined {room_name}"}, room=room_name)

async def create_match( currLevel):
    print(f"*******************************")
    print(active_students)
    print(connected_clients)
    if len( active_students[currLevel]) > 1:
        # pop the last two elements and then add them into a room, notify them and finaly start the match ...
        player_1 = active_students[currLevel].pop()
        player_2 = active_students[currLevel].pop()

        currRoom = create_room()
        await join_room( player_1, currRoom)
        await join_room( player_2, currRoom)
        # match_count += 1
        # await sio.emit(f"NEW MATCH: {match_count} between {player_1} and {player_2}")
    
active_students = defaultdict( list )
@sio.event
async def connect(sid, env, *args):
    print(f"Student: {sid} connected")
    query_string = env.get("QUERY_STRING", "")
    query_params = parse_qs(query_string)
    print("1")
    NU_ID = query_params.get("NU_ID", ["XXXXXXXXX"])[0]
    MAIL_ID = query_params.get("MAIL_ID", ["guest@northeastern.com"])[0]
    print("2")
    connected_clients[sid] = {
        "NU_ID":NU_ID,
        "MAIL_ID":MAIL_ID,
    }
    print("3")
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
async def message():
    # await sio.emit("Prajwal this is a response.")
    print("Here for good...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

