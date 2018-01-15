# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
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
instruct = ""
timer_interval = 1000
displayed = True

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
            #print "Invalid card: ", suit, rank

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
        
# define hand class
class Hand:
    def __init__(self):
        self.hlist = []	# create Hand object

    def __str__(self):
        build = ""
        if len(self.hlist) > 0:
            for i in self.hlist:
                build = build + i.get_suit() + i.get_rank()+ " "
        return 'Hand contains ' + build

    def add_card(self, card):
        self.hlist.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        total = 0
        aces=0
        for i in self.hlist:
            rank = i.get_rank()
            total += VALUES[rank]
            if rank == 'A':
                aces += 1
        if aces == 0:
            return total
        elif total + 10 <= 21:
            return total + 10
        else:
            return total
        
    def draw(self, canvas, pos):      
        n = 1
        pos_orig_x = pos[0]
        pos_orig_y = pos[1]
            
        for i in self.hlist:
            if n == 6:
                pos[0] = pos_orig_x
                pos[1] = pos_orig_y+ CARD_SIZE[1]+5
            i.draw(canvas,pos)
            pos = [pos[0]+CARD_SIZE[0]*1.5,pos[1]]
            n += 1
# define deck class 
class Deck:
    def __init__(self):
        self.dlist = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card1 = Card(suit,rank)
                self.dlist.append(card1)
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.dlist)    # use random.shuffle()
        
    def deal_card(self):
        return self.dlist.pop(-1)	# deal a card object from the deck
    
    def __str__(self):
        build = ""
        for i in self.dlist:
            build = build + i.get_suit() + i.get_rank()+ " "
        return 'Deck contains ' + str(build)        

#define event handlers for buttons
def deal():
    global outcome, in_play,deck1,player1,dealer1,score
    deck1 = Deck()
    player1 = Hand()
    dealer1 = Hand()
    deck1.shuffle()
    
    player1.add_card(deck1.deal_card())
    player1.add_card(deck1.deal_card())
    dealer1.add_card(deck1.deal_card())
    dealer1.add_card(deck1.deal_card())
  
    if in_play == True:
        outcome = 'Player forfeited last game!'
        score -= 1
    else:
        outcome = 'Game started'
    
    in_play = True

def hit():
    global in_play,score,outcome
    current_value = player1.get_value()
    # if the hand is in play, hit the player
    if in_play and current_value <= 21:
        player1.add_card(deck1.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player1.get_value() > 21:
            outcome = 'Player Busted! Dealer wins!'
            in_play = False
            score -= 1
    else:
        outcome = 'Sorry, but game is over!'

def stand():
    global in_play,outcome,score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        outcome = 'Sorry, but game is over!'
    else:
        while dealer1.get_value() < 17:
            dealer1.add_card(deck1.deal_card())
        dval = dealer1.get_value()
        pval = player1.get_value()
        if dval > 21:
            outcome = 'Dealer Busted! You Win!'
            score += 1
        elif dval > pval:
            outcome = 'Dealer Wins!'
            score -= 1
        elif dval == pval:
            outcome = 'Tie, Dealer Wins!'
        else:
            outcome = 'Player Wins!'
            score += 1
    # assign a message to outcome, update in_play and score
        in_play = False

# draw handler    
def draw(canvas):
    global instruct
    canvas.draw_text('BLACKJACK',[50,75],50,'RED')
    canvas.draw_text('score: '+str(score),[500,50],25,'white')
    canvas.draw_text('Dealer',[50,175],25,'Black')
    canvas.draw_text(str(outcome),[200,150],35,'white')
    dealer1.draw(canvas,[50,200])
    canvas.draw_text('Player',[50,375],25,'black')
    player1.draw(canvas,[50,400])
    canvas.draw_text(str(instruct),[200,375],35,'white')
    
    if in_play == False:
        if displayed:
            instruct = 'Click Deal for new game'
        else:
            instruct = ""
    else:
        instruct = 'Hit or Stand?'
        canvas.draw_image(card_back,CARD_BACK_CENTER , CARD_BACK_SIZE, [CARD_BACK_CENTER[0]+50,CARD_BACK_CENTER[1]+200], CARD_BACK_SIZE)

def timer_handler():
    global displayed
    displayed = not displayed
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
timer = simplegui.create_timer(timer_interval, timer_handler)

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
timer.start()

# remember to review the gradic rubric