# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 15
PAD_WIDTH = 10
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = True
RIGHT = False
ball_pos = [WIDTH / 2, HEIGHT /2]
ball_vel = [0,0]
paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT /2]
    # if direction is RIGHT, the ball's velocity is upper right, else upper left
    if direction:
        ball_vel [0] = - random.randrange(2, 4)
        ball_vel [1] = - random.randrange(1, 3)
    else:
        ball_vel [0] = random.randrange(2, 4)
        ball_vel [1] = - random.randrange(1, 3)

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    #Call fuction spawn_ball to get the ball in a new game mode
    spawn_ball(LEFT)
       
        
# define event handlers

# draw 
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

     # draw ball
    ball = canvas.draw_circle(ball_pos, BALL_RADIUS, 2, 'White', 'White')

    # update ball
    ball_pos [0] += ball_vel[0]
    ball_pos [1] += ball_vel[1]

    # determine whether paddle and ball collide 
    a = ball_pos [0] + BALL_RADIUS
    b = ball_pos [0] - BALL_RADIUS
    y = ball_pos [1] + BALL_RADIUS
    z = ball_pos [1] - BALL_RADIUS
    if a > WIDTH - PAD_WIDTH and y >= paddle1_pos and z <= paddle1_pos + PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0]*1.1
        ball_vel[1] = -ball_vel[1]*1.1
    elif b < PAD_WIDTH and y >= paddle2_pos and z <= paddle2_pos + PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0]*1.1
        ball_vel[1] = -ball_vel[1]*1.1
        
    # determine a goal 
    elif a >= WIDTH - PAD_WIDTH:
        spawn_ball(LEFT)
        score2 += 1     
    elif b <= PAD_WIDTH:
        spawn_ball(RIGHT)
        score1 += 1

    #keep ball on the screen (vertically)
    if ball_pos [1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos [1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
     # draw paddles
    paddle1 = canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle1_pos], 
                               [WIDTH - HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], 
                               PAD_WIDTH, 'White')
    paddle2 = canvas.draw_line([HALF_PAD_WIDTH, paddle2_pos], 
                               [HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], 
                               PAD_WIDTH, 'White')

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >=0 and paddle1_pos + PAD_HEIGHT + paddle1_vel <= HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >=0 and paddle2_pos + PAD_HEIGHT + paddle2_vel <= HEIGHT:
        paddle2_pos += paddle2_vel
 
    # draw scores
    player1 = canvas.draw_text("Player_1 "+str(score1), [WIDTH/2 + 20, 20], 18, "White")
    player2 = canvas.draw_text("Player_2 "+str(score2), [WIDTH/2 - 100, 20], 18, "White")
   

"""Key handlers to move the paddles"""
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP['W']:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP['down']: 
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP['S']:
        paddle2_vel = 3
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['W']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']: 
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['S']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New game", new_game)

# start frame
new_game()
frame.start()
    

