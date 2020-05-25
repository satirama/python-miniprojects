# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

"""Import necessary modules"""
import simplegui
import random
import math

"""Global variables"""
secret_number = random.randrange(0,100)
n=100
m=0
remaining_guess = math.log(n-m+1) / math.log (2)
r_g = int(math.ceil(remaining_guess))

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    print "Start guessing numbers."
    global secret_number, n, m, remaining_guess, r_g
    secret_number = random.randrange(m,n)
    remaining_guess = math.log(n-m+1) / math.log (2)
    r_g = int(math.ceil(remaining_guess))
    print "You have", r_g, "remaining guesses."
    print
    
  
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    # remove this when you add your code    
    global secret_number,n,m
    n=100
    m=0
    secret_number = random.randrange(m,n)
    print "Pick a number between 0 and 99."
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number,n,m
    n=1000
    m=0
    secret_number = random.randrange(m,n) 
    print "Pick a number between 0 and 999."
    new_game()

#Main logic of the game
def input_guess(guess):
    print "Your guess was",guess
    g = int(guess)
    global r_g
    r_g -= 1
    if g < secret_number and r_g>0:
        print "Higher!"
        print "You have",r_g,"remaining guesses."
        print
    elif g > secret_number and r_g>0:
        print "Lower!"
        print "You have",r_g,"remaining guesses."
        print
    elif g == secret_number and r_g>=0:
        print "Ding! Got it."
        print
        new_game()
    elif r_g == 0:
        print "You ran out of guesses. Try again."
        print
        new_game()
    else:
        print "Wrong input!"
        
# create frame and events
frame = simplegui.create_frame("Guess it",300,300)
inp = frame.add_input("Guess the number...", input_guess ,200)
newgame_100 = frame.add_button("Range is [0,100)",range100)
newgame_1000 = frame.add_button("Range is [0,1000)", range1000)

# register event handlers for control elements and start frame
# Event handler


# call new_game 
new_game()

# Frame start
frame.start()


# always remember to check your completed program against the grading rubric
