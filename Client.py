#Important libraries for sending/receiving information to a server
import socket, pickle

#Important library necessary for the chess graphics
import pygame as pg

#Important library useful for updating the client periodically
from time import time

#Initialise pygame
pg.init()

#Initializes a pygame screen of size 1200 by 700 with the caption: multiplayer chess
screenSize = (1200, 700)
screen = pg.display.set_mode(screenSize)
pg.display.set_caption("Multiplayer Chess")

#Initialises the pygame clock
clock = pg.time.Clock()

#Defines various colours useful in the game
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
GREEN    = (  0, 255,   0)
BROWN    = (165,  42,  42)
ORANGE   = (255, 165,   0)
YELLOW   = (255, 255,   0)

#Defines the size, and border of the chess board
tileSize = 60
border = 25

#Defines the fonts used
pieceFont = pg.font.Font("freesansbold.ttf", 30)
subtitleFont = pg.font.Font("freesansbold.ttf", 25)
notationFont = pg.font.Font("freesansbold.ttf", 15)

#Initialises the moveNotation list which stores the moves that the moveHistory button will display
moveNotation = list()

#Initialises the alertMessage which stores the message that the alerts button will display
alertMessage = None

#Button class
class button(pg.sprite.Sprite):

    #Constructor for a basic button
    def __init__(self, topLeft, bottomRight, colour, name):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface( (bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]) )
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = topLeft

        self.name = name

    #Displays the button and it's name
    def display(self):

        screen.blit(self.image, self.rect)

        #Displays the button's name if it is defined
        if self.name != None:
            text = pieceFont.render(self.name, True, ORANGE)
            textRect = text.get_rect()
            textRect.center = ((self.rect.left + self.rect.right)/2, (self.rect.bottom + self.rect.top)/2)
            screen.blit(text, textRect)

    #Displays the list of moves played (only used for moveHistory button)
    def displayMoves(self, moveNotation):

        screen.blit(self.image, self.rect)

        #Displays the title White Moves
        text = subtitleFont.render("White Moves", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.rect.left + 1/4*(self.rect.right - self.rect.left), self.rect.top + 20)
        screen.blit(text, textRect)

        #Displays the title Black Moves
        text = subtitleFont.render("Black Moves", True, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.rect.left + 3/4*(self.rect.right - self.rect.left), self.rect.top + 20)
        screen.blit(text, textRect)

        #If there are too many moves to display, it does not display the first few moves
        moveNum = 1
        while 16 * (len(moveNotation[2*(moveNum - 1):]) + 1)/2 + 61 > self.rect.bottom:
            moveNum += 1

        #Alternates between displaying a move on the left side then the right side
        num = 1
        for move in moveNotation[2*(moveNum - 1):]:

            if num % 2 == 1:
                text = notationFont.render(str(moveNum) + ". " + move, True, BLACK)
                textRect = text.get_rect()
                textRect.topleft = (self.rect.left + 5, border + (num + 1)/2 * 16 + 20)

            elif num % 2 == 0:
                text = notationFont.render(move, True, BLACK)
                textRect = text.get_rect()
                textRect.topleft = (self.rect.left + 1/2*(self.rect.right - self.rect.left) + 5, border + num * 8 + 20)

                moveNum += 1

            screen.blit(text, textRect)
            num += 1

    #Displays the alertMessage (only used for alerts button)
    def displayAlert(self, alertMessage):

        screen.blit(self.image, self.rect)
        
        if alertMessage != None:
            if alertMessage == "Game Drawn":
                msg = "Game Drawn"
                
            elif alertMessage[0] == WHITE:
                msg = "White " + alertMessage[1]
            else:
                msg = "Black " + alertMessage[1]
                
            text = pieceFont.render(msg, True, WHITE)
            textRect = text.get_rect()
            textRect.midleft = (self.rect.left + 10, (self.rect.top + self.rect.bottom)/2)
            screen.blit(text, textRect)
        

    #Returns if the button is clicked
    def clicked(self, mousePos):
        if self.rect.left < mousePos[0] and self.rect.right > mousePos[0]:
            if self.rect.top < mousePos[1] and self.rect.bottom > mousePos[1]:
                return True

#Creates a class for each chess tile
class chessTile(pg.sprite.Sprite):

    #Constructor
    def __init__(self, coordinate):
        pg.sprite.Sprite.__init__(self)

        #Checks whether the colour of the tile is white or black
        if (coordinate[0] + coordinate[1]) % 2 == 0:
            self.colour = WHITE
        else:
            self.colour = BLACK

        self.image = pg.Surface((tileSize, tileSize))
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = (2*border + coordinate[0]*tileSize, 2*border + coordinate[1]*tileSize)

        self.coordinate = coordinate

    #Returns true if the chess tile was clicked
    def clicked(self, mousePos):
        if self.rect.left < mousePos[0] and self.rect.right > mousePos[0]:
            if self.rect.top < mousePos[1] and self.rect.bottom > mousePos[1]:
                return True

    #Displays the button, the piece on it, and whether it is clicked and/or potential chess move
    def display(self, legalMoves):

        #Changes the colour of the tile based on whether the piece is selected, or a possible move
        if len(legalMoves) == 0:
            self.image.fill(self.colour)

        elif self.coordinate == legalMoves[0][:2]:
            self.image.fill(GREEN)

        else:
            for coord in legalMoves[1:]:
                if self.coordinate == coord[:2]:
                    self.image.fill(RED)
                    break

        #Displays the tile
        screen.blit(self.image, self.rect)

        #Displays the piece's letter
        if pieceDict[ self.coordinate ] != None:

            if pieceDict[ self.coordinate ][0] == WHITE:
                text = pieceFont.render( pieceDict[self.coordinate][1], True, BLUE )
            else:
                text = pieceFont.render( pieceDict[self.coordinate][1], True, ORANGE )

            textRect = text.get_rect()
            textRect.center = ( 2*border + tileSize*(self.coordinate[0] + 0.5), 2*border + tileSize*(self.coordinate[1] + 0.5) )
            
            screen.blit(text, textRect)

#This class defines a network that will connect to the server
class Network:
    #Constructor that creates a socket which connects to a specific addresse
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = input("Input the IP Addresse of the Server")
        self.port = 5555
        self.addr = (self.server, self.port)

    #Function that connects the socket to the server, returning the user's colour
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads( self.client.recv(1024) )
        except:
            pass

    #Sends information the server, and receives a reply back
    def send(self, data):
        try:
            self.client.send( pickle.dumps(data) )
            return pickle.loads( self.client.recv(1024) )
        except socket.error as e:
            print(e)

#Creates a Network named connection, and connects it to the server
connection = Network()
pieceDict, msg = connection.connect()
print (msg)

#Creates the chess board
tiles = pg.sprite.Group()
for coordinate in pieceDict.keys():
    tiles.add(chessTile(coordinate))  

#Creates the moveHistory, and timer widgets
moveHistory = button( (4*border + 8*tileSize, border), (screenSize[0] - border, 8*tileSize - border),  ORANGE, None)

#Stores the maximum lengh of the button
length = screenSize[0] - (5*border + 8*tileSize)

#Creates the resign, draw, and undo buttons
resign = button( (4*border + 8*tileSize,              8*tileSize - border), ( 4*border + 8*tileSize + 1/3*length, 8*tileSize + 3*border),    RED, "Resign")
draw   = button( (4*border + 8*tileSize + 1/3*length, 8*tileSize - border), ( 4*border + 8*tileSize + 2/3*length, 8*tileSize + 3*border), YELLOW,   "Draw")
undo   = button( (4*border + 8*tileSize + 2/3*length, 8*tileSize - border), ( screenSize[0] - border,             8*tileSize + 3*border),  BLACK,   "Undo")
alerts = button( (border, 8*tileSize + 4*border), (screenSize[0] - border, screenSize[1] - border), BLACK, None)

#Updates the screen
def update_screen(legalMoves):

    #Fills the screen with white
    screen.fill(WHITE)

    #Displays the chessboard background
    pg.draw.rect(screen, BROWN, (border, border, 8*tileSize + 2*border, 8*tileSize + 2*border))

    #Displays the chess tiles
    for tile in tiles:
        tile.display(legalMoves)

    #Displays the various buttons on the screen
    moveHistory.displayMoves(moveNotation)
    resign.display()
    draw.display()
    undo.display()
    alerts.displayAlert(alertMessage)

    #Updates the display
    pg.display.flip()

    #Sets the refresh to 30 ticks per second
    clock.tick(15)

#Gets user input
def userInput(legalMoves):
    global pieceDict, moveNotation, alertMessage

    for event in pg.event.get():

        #If the user quits, the program ends
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
            quit()

        #If the user clicks the mouse buttons
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousePos = pg.mouse.get_pos()
            if resign.clicked(mousePos):
                alertMessage = connection.send("Resign")
                
            elif draw.clicked(mousePos):
                alertMessage = connection.send("Draw")
                
            elif undo.clicked(mousePos):
                alertMessage = connection.send("Undo")
                
            else:
                for tile in tiles:
                    if tile.clicked(mousePos):
                        data = connection.send(tile.coordinate)
                        if data != "Wrong Turn":
                            alertMessage, legalMoves, pieceDict, moveNotation = data

                        break

    return legalMoves

legalMoves = list()
start = time()

#Loops indefinitely
while 1:
    legalMoves = userInput(legalMoves)
    update_screen(legalMoves)
    
    #Updates the screen every 0.25 seconds for the other player's actions
    if time() - start > 0.25:
        alertMessage, pieceDict, moveNotation = connection.send("Update")
        start = time()
            
