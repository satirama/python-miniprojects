# template for "Stopwatch: The Game"
#import modules
import simplegui

# define global variables
WIDTH = 300
LENGTH = 300
T = 0
C = 0
R = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global T
    s_t = str(T)
    l_t = len(s_t)
    if T < 600:
        if l_t <= 2:
            return "0:0" + str(T/10.0)
        elif l_t == 3:
            return "0:" + str(T/10.0)
    elif T >= 600:
        seconds = T%600/10.0
        minutes = str(T//600)
        if seconds < 10:
            return minutes + ":0" + str(seconds)
        elif seconds >= 10:
            return minutes + ":" + str(seconds)   
          
# define function for the score counter
def count():
    global T, C, R
    return str(R) + "/" + str(C)            
            
  
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    timer.start()
    
def stop_button():
    global T,C,R
    if timer.is_running():
        timer.stop()
        C += 1
        if T % 10 == 0:
            R += 1
        else:
            R += 0
    else: 
        timer.stop()

def reset_button():
    timer.stop()
    global T, C, R
    T = 0
    C = 0
    R = 0

# define event handler for timer with 0.1 sec interval
def time_handler():
    global T
    T += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(T), [WIDTH//4,LENGTH//2], 50, 'White')
    canvas.draw_text(count(), [WIDTH*.75,LENGTH*.1], 15, 'Yellow')
    
# create frame
frame = simplegui.create_frame("Timer game",WIDTH,LENGTH)

# register event handlers
timer = simplegui.create_timer(100,time_handler)
clock = frame.set_draw_handler(draw_handler)
button1 = frame.add_button('Start', start_button)
button2 = frame.add_button('Stop', stop_button)
button3 = frame.add_button('Reset', reset_button)

# start frame
timer.stop()
frame.start()

# Please remember to review the grading rubric
