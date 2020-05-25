# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_v = 0
dealer_v = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def draw_back(self, canvas, pos):
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
    # return a string representation of a hand
        if len(self.hand) > 0:
            text = ""
            for i in range(len(self.hand)):
                text += str(self.hand[i]) + " "
            return "hand contains " + text + "."
        else:
            return "Empty hand"

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        # sum of the hand value
        value = 0
        rank = []
        for i in range(len(self.hand)):
            value += VALUES.get(self.hand[i].get_rank())
        for i in range(len(self.hand)):
            rank += self.hand[i].get_rank()
        if "A" not in rank:
            return value
        else:
            if value + 10 <= 21: 
                return value + 10
            else:
                return value
            
    def draw(self, canvas, pos):
    # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand)): 
            self.hand[i].draw(canvas, [pos[0] + i * 80, pos[1]])                    
           
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        deck =[]
        for s in SUITS:
            for r in RANKS:
                deck.append(Card(s, r))
        self.deck = deck

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        dealt = self.deck[-1]
        self.deck.pop()
        return dealt
    
    def __str__(self):
        # return a string representing the deck
        text = ""
        for i in range(len(self.deck)):
            text += str(self.deck[i]) + " "
        return "Deck is " + text


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_h, player_h, score, player_v
    
    # your code goes here
    deck = Deck()
    deck.shuffle()
    dealer_h = Hand()
    player_h = Hand()
    dealer_h.add_card(deck.deal_card())
    dealer_h.add_card(deck.deal_card())
    player_h.add_card(deck.deal_card())
    player_h.add_card(deck.deal_card())   
    outcome = "Hit or Stand?"
    player_v = player_h.get_value()
    
    if in_play:
        score += -1
        outcome = "Player looses."
    in_play = True

def hit():
    # if the hand is in play, hit the player
    global in_play, deck, player_h, player_v, score, outcome
    if in_play:
        player_h.add_card(deck.deal_card())
        if player_h.get_value() <= 21:
            player_v = player_h.get_value()
            return player_v
    
    # if busted, assign a message to outcome, update in_play and score
        else:
            outcome = "Busted!"
            in_play = False
            score += -1
    else:
        outcome = "New deal?"
       
def stand():  
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global in_play, deck, dealer_h, dealer_v, score, player_v, outcome
    if in_play:
        dealer_v = dealer_h.get_value()
        player_v = player_h.get_value()
        while dealer_v < 17:
            dealer_h.add_card(deck.deal_card())
            dealer_v = dealer_h.get_value()
    # assign a message to outcome, update in_play and score   
        if dealer_v > 21:
                outcome = "Dealer's busted. You win!"
                in_play = False
                score += 1
        else:
            if dealer_v >= player_v:
                    outcome = "The house wins."
                    in_play = False
                    score += -1                
            else:
                    outcome = "You win!!"
                    in_play = False
                    score += 1
    else:
        outcome = "New deal?"

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("H", "9")
    card.draw_back(canvas, [280, 300])
    player_h.draw(canvas, [50,450])
    dealer_h.draw(canvas, [100, 50])
    canvas.draw_text(outcome, [390,350], 20, "White")
    canvas.draw_text("Score: " + str(score), [390,375], 15, "White")
    canvas.draw_text("Blackjack", [70,300], 40, "Black")
    canvas.draw_text("(" + str(player_v) + ")", [60,440], 12, "Red")   
    canvas.draw_text("(" + str(dealer_v) + ")", [110,160], 12, "Red")   

    if in_play:
        card.draw_back(canvas, [180, 50])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric