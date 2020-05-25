# Polyline drawing problem

###################################################
# Student should enter code below

import simplegui
import math

polyline = []

# define mouseclick handler
def click(pos):
    global polyline
    polyline.append(pos)
    
          
# button to clear canvas
def clear():
    global polyline
    polyline = []

# define draw
def draw(canvas):
    if len(polyline) > 0:
        canvas.draw_polyline(polyline, 10, "Purple")
    
# create frame and register handlers
frame = simplegui.create_frame("Echo click", 300, 200)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_button("Clear", clear)

# start frame
frame.start()

