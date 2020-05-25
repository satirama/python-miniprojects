import simplegui

# Initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [-40.0 / 6,  5.0 / 6]

# define event handlers
def draw(canvas):
    # Update ball position
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    
    # collide and reflect off of left hand side of canvas
    if ball_pos[0] <= BALL_RADIUS:
        vel[0] = - vel[0]   
        
    # collide and reflect off of right hand side of canvas
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        vel[0] = - vel[0]
        
    # collide and reflect off of top hand side of canvas
    if ball_pos[1] <= BALL_RADIUS:
        vel[1] = - vel[1]   
        
    # collide and reflect off of right hand side of canvas
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        vel[1] = - vel[1]
        
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

# create frame
frame = simplegui.create_frame("Ball physics", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()
