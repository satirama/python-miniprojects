# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global state, counter, exp, exposed, index1, index2, memory_deck
    memory_deck = range(8)*2
    random.shuffle(memory_deck)
    state = 0 
    counter = 0
    index1 = []
    index2 = []
    exposed = [False for i in range(16)]
    label.set_text("Turns = " + str(counter))
     

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, index1, index2, counter
    card = pos[0] // 50
    if exposed[card] == False:
        exposed[card] = True
        if state == 0:
            state = 1
            index1 = card
        elif state == 1:
            state = 2
            counter += 1
            label.set_text("Turns = " + str(counter))
            index2 = card
        else:
            if memory_deck[index1] != memory_deck[index2]:
                exposed[index1] = False
                exposed[index2] = False
            index2 = []
            index1 = card
            state = 1
                    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card in range(len(memory_deck)):
        if exposed [card]:
            canvas.draw_text(str(memory_deck[card]), [5 + 50*card,80],80,"White")
        else:
            canvas.draw_polygon([[50*card,0],[50*card,100], [50 + 50*card,100],
                                 [50 + 50*card,0]], 5,"Black","Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric