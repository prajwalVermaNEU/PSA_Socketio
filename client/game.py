from tkinter import Canvas
import random

WIDTH = 800
HEIGHT = 600
IN_GAME = True
SEG_SIZE = 20
GAME_MODE = True
c = None
currSnake = None
opponentSnake = None

def create_apple( c, apple_pos = None):
    global APPLE, apple_posx, apple_posy
    apple_posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) // SEG_SIZE) if apple_pos is None else apple_pos[0]
    apple_posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) // SEG_SIZE) if apple_pos is None else apple_pos[1]
    APPLE = c.create_oval(apple_posx, apple_posy, apple_posx + SEG_SIZE, apple_posy + SEG_SIZE, fill="red")

class Segment(object):
    def __init__(self, c, x, y, color=None):
        self.x, self.y = x, y
        if not color:
            self.instance = c.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill="white")
        else:
            self.instance = c.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill=color)
    
    def getCoords(self):
        return (self.x, self.y)

class Snake(object):
    def __init__(self, c, segments, color=None):
        self.c = c
        self.segments = segments
        self.color = color
        # Possible directions of movement
        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.mapping["Right"]

    # Snake movement
    def move(self):
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = self.c.coords(self.segments[index + 1].instance)
            self.c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = self.c.coords(self.segments[-2].instance)
        self.c.coords(
            self.segments[-1].instance,
            x1 + self.vector[0] * SEG_SIZE, y1 + self.vector[1] * SEG_SIZE,
            x2 + self.vector[0] * SEG_SIZE, y2 + self.vector[1] * SEG_SIZE
        )

        # for segment in self.segments:
        #     segment.x, segment.y = self.c.coords(segment.instance)[:2]

    # Snake getting fatter: Adding a segment to the snake body
    def add_segment(self, color=None):
        last_seg = self.c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y, color))
            
    # Change of direction initiated by AI
    def change_direction_ai(self, direction):
        if direction in self.mapping:
            #print("changing direction to:", direction)
            self.vector = self.mapping[direction]

    def reset_snake(self):
        for segment in self.segments:
            self.c.delete(segment.instance)
    
    def getAllCoords(self):
        result = []
        for segment in self.segments:
            # print( '#################### THIS MUST WORK::::', s )
            real_coords = self.c.coords(segment.instance)
            result.append( real_coords )
        return result

    def updateSnake(self, positions):
        self.reset_snake()
        new_segments = []
        for x,y,_,_ in positions:
            new_segments.append( Segment( self.c, x, y, "red"))
        self.segments = new_segments

def create_snake( c, color = None):
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) // SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) // SEG_SIZE)
    segments = [Segment( c, posx, posy, color), Segment( c, posx + SEG_SIZE, posy, color), Segment( c, posx + SEG_SIZE*2, posy, color)]
    return Snake( c, segments, color)

def main():
    global GAME_MODE, IN_GAME, APPLE, apple_posx, apple_posy, currSnake, opponentSnake, c
    currSnake.move()
    currSnakeCoors = c.coords(currSnake.segments[-1].instance)

    def check_boundary_collision( givenCoords ):
        x1, y1, x2, y2 = givenCoords
        return x1 < 0 or y1 < 0 or x2 > WIDTH or y2 > HEIGHT


    def check_self_collision(snake):
        head_coords = c.coords(snake.segments[-1].instance)
        for segment in snake.segments[:-1]:  # Ignore the head
            if c.coords(segment.instance) == head_coords:
                return True
        return False

    # Check if a snake collides with the other snake
    def check_snake_collision(snake1, snake2):
        head_coords = c.coords(snake1.segments[-1].instance)
        for segment in snake2.segments:
            if c.coords(segment.instance) == head_coords:
                return True
        return False

    # Check collisions for yellow snake
    if(
        check_boundary_collision(currSnakeCoors) or 
        check_self_collision(currSnake) or 
        ( opponentSnake is not None and check_snake_collision(currSnake, opponentSnake) )
    ):
        IN_GAME = False
        print("Snake DIED")
        game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="Game over!", font='Arial 20', fill='red', state='hidden')
        c.itemconfigure(game_over_text, text="Game Over! ", state='normal')
        return {
            "STATUS": "GAME-OVER"
        }

    direction = None
    if random.randint(1, 10) == 1:
        direction = random.choice(["Up", "Down", "Right", "Left"])
        currSnake.change_direction_ai(direction)
                
    
    if currSnakeCoors == c.coords(APPLE):
        currSnake.add_segment()
        c.delete(APPLE)
        create_apple()
    
    return {
        "STATUS": "IN-GAME"
    }

def update_opponent_data(position):
    global opponentSnake
    if opponentSnake is not None and c is not None:
        # c.coords(opponentSnake.segments[-1].instance, x1, y1, x2, y2)
        opponentSnake.updateSnake(position)

def getCurrSnake():
    global currSnake
    return currSnake

def createGame( root, apple_pos ):    
    global currSnake, opponentSnake, c
    
    c = Canvas( root, width=WIDTH, height=HEIGHT, bg="#003300")
    c.grid()
    create_apple( c, apple_pos )
    currSnake, opponentSnake = create_snake( c, "green" ), create_snake(c, "red")

    # print( "########################", currSnake.segments)
