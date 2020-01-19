# Name        : Server for Chess Program
# Author      : Timmy Thorpe
# Description : A server that can send information between two clients for a chess game

#Important libraries for sending/receiving information to clients
import socket, pickle

#Unique library created by Timmy Thorpe which contains functions for determining the legalMoves that a chess piece may conduct
import chess

#_thread is necessary for communicating between multiple clients simultaneously
from _thread import *

#Colours for white & black
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

#Letter to number converter
Num2Letter = {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}

#Dictionary with all the original positions of chess pieces, and their colours
pieceDict = {
            (0, 0) : (BLACK, "R"), (1, 0) : (BLACK, "N"), (2, 0) : (BLACK, "B"), (3, 0) : (BLACK, "Q"), (4, 0) : (BLACK, "K"), (5, 0) : (BLACK, "B"), (6, 0) : (BLACK, "N"), (7, 0) : (BLACK, "R"),
            (0, 1) : (BLACK, "P"), (1, 1) : (BLACK, "P"), (2, 1) : (BLACK, "P"), (3, 1) : (BLACK, "P"), (4, 1) : (BLACK, "P"), (5, 1) : (BLACK, "P"), (6, 1) : (BLACK, "P"), (7, 1) : (BLACK, "P"),
            (0, 2) :         None, (1, 2) :         None, (2, 2) :         None, (3, 2) :         None, (4, 2) :         None, (5, 2) :         None, (6, 2) :         None, (7, 2) :         None,
            (0, 3) :         None, (1, 3) :         None, (2, 3) :         None, (3, 3) :         None, (4, 3) :         None, (5, 3) :         None, (6, 3) :         None, (7, 3) :         None,
            (0, 4) :         None, (1, 4) :         None, (2, 4) :         None, (3, 4) :         None, (4, 4) :         None, (5, 4) :         None, (6, 4) :         None, (7, 4) :         None,
            (0, 5) :         None, (1, 5) :         None, (2, 5) :         None, (3, 5) :         None, (4, 5) :         None, (5, 5) :         None, (6, 5) :         None, (7, 5) :         None,
            (0, 6) : (WHITE, "P"), (1, 6) : (WHITE, "P"), (2, 6) : (WHITE, "P"), (3, 6) : (WHITE, "P"), (4, 6) : (WHITE, "P"), (5, 6) : (WHITE, "P"), (6, 6) : (WHITE, "P"), (7, 6) : (WHITE, "P"),
            (0, 7) : (WHITE, "R"), (1, 7) : (WHITE, "N"), (2, 7) : (WHITE, "B"), (3, 7) : (WHITE, "Q"), (4, 7) : (WHITE, "K"), (5, 7) : (WHITE, "B"), (6, 7) : (WHITE, "N"), (7, 7) : (WHITE, "R")
            }

#Defines the current positions of the white and black kings
kingPositions = {WHITE : (4, 7), BLACK : (4, 0)}

#Current turn
currentTurn = WHITE

#Initialises the moveList which stores all the previously made moves, and the lastMove which stores the previous move
moveList = list(); lastMove = None

#Initialises the moveNotation list which stores the moves made in a form that can be displayed
moveNotation = list()

#Initialises the legalMoves list which stores all the possible moves that a piece may make
#The first item in the legalMoves list is always the piece selected
legalMoves = list()

#Initialises alertMsg which stores the different messages that may be sent to the clients (ex. white resigns)
alertMsg = None

#Sets the IP addresse and port of the server
#The server must be changed depending on the local network
server = socket.gethostbyname(socket.gethostname())
port = 5555

#Creates a socket as s, and binds that socket to a specific IP and port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server, port))

#Only 2 clients may connect to the server port at once (white & black players respectively)
s.listen(2)

#Debugging messages
print("Waiting for a connection, Server Started")
print("IP Addresse of Server :", server)

#Creates a threaded client
def threaded_client(conn, currentPlayer):
    #Allows the function to modify these variables
    global currentTurn, pieceDict, kingPositions, moveList, lastMove, moveNotation, legalMoves, alertMsg

    #When connecting to a client, the server tells them which player they are
    #White is the player that connects first, and black is the player that connects after
    if currentPlayer == WHITE:
        conn.sendall( pickle.dumps( (pieceDict, "You are white") ) )
    else:
        conn.sendall( pickle.dumps( (pieceDict, "You are black") ) )

    #Loops indefinitely
    while 1:
        try:
            #Recieves data from the client
            data = pickle.loads( conn.recv(1024) )

            #If the client sends nothing, the connection disconnects, and the thread exits
            if not data:
                print("Disconnected")
                break

            #If the game is over, no further input from the clients is accepted
            elif (lastMove != None and (lastMove == "stalemate" or lastMove == "checkmate")) or (alertMsg != None and (alertMsg == "Game Drawn" or alertMsg[1] == "resigns.")):
                pass

            #If the data sent is Resign, it sets the alertMsg as the current player resigns
            elif data == "Resign":
                alertMsg = (currentPlayer, "resigns.")
                conn.sendall( pickle.dumps(alertMsg) )

            #If the data sent is Draw
            elif data == "Draw":

                #If no current alertMsg exists or the other player is not proposing a draw
                #The alertMsg proposes a draw from the current player
                if alertMsg == None  or alertMsg[1] != "proposes a draw.":
                    alertMsg = (currentPlayer, "proposes a draw.")

                #If the alertMsg currently proposes a draw from the same player
                #The alertMsg is set to None
                elif alertMsg[0] == currentPlayer:
                    alertMsg = None

                #Otherwise, the alertMsg is set to Game Drawn, indicating that both players have agreed to a draw
                else:
                    alertMsg = "Game Drawn"

                #Sends the alertMsg to the client
                conn.sendall( pickle.dumps(alertMsg) )

            #If the data recieved from the client is undo
            elif data == "Undo":
                
                #If there are no moves to undo, it sets alertMsg to None
                if lastMove == None:
                    alertMsg = None

                #If no current alertMsg exists or the other player is not proposing a draw
                #The alertMsg proposes a draw from the current player
                elif alertMsg == None or alertMsg[1] != "wishes to undo.":
                    alertMsg = (currentPlayer, "wishes to undo.")

                #If the alertMsg currently proposes an undo from the same player
                #The alertMsg is set to None
                elif alertMsg[0] == currentPlayer:
                    alertMsg = None

                #Otherwise, if the other player agrees to the other's wish to undo
                else:
                    #Sets the alertMsg to nothing
                    alertMsg = None

                    #Reverses the last move, modifying the pieceDict which stores all the users moves
                    pieceDict[lastMove[0]] = lastMove[1]
                    pieceDict[lastMove[2]] = lastMove[3]

                    #Accounts for special cases
                    if lastMove[-1] == "ep":
                        pieceDict[lastMove[2]] = (currentTurn, "P")
                    elif lastMove[-1] == "O-O":
                        pieceDict[(7, lastMove[0][1])] = (currentTurn, "P")
                    elif lastMove[-1] == "O-O-O":
                        pieceDict[(0, lastMove[0][1])] = (currentTurn, "P")

                    #Removes the last item form the moveList, and moveNotation dictionaries
                    moveList.pop(-1)
                    moveNotation.pop(-1)

                    #Sets the lastMove equal to the last item in the moveList, if no such move exists it sets it as None
                    if len(moveList) == 0:
                        lastMove = None
                    else:
                        lastMove = moveList[-1]

                    #Changes the currentTurn
                    if currentTurn == WHITE:
                        currentTurn = BLACK
                    else:
                        currentTurn = WHITE

                #Send the alertMsg back to the user
                conn.sendall( pickle.dumps(alertMsg) )

            #If the client requests an update, it sends the client necessary information
            elif data == "Update":
                conn.sendall( pickle.dumps( (alertMsg, pieceDict, moveNotation) ) )

            #If it is the currentPlayer's turn to move
            elif currentPlayer == currentTurn:

                #If the client is not currently selecting a piece to move
                if not len(legalMoves):
                        
                    #Based on the tile clicked, it finds its legal moves
                    if pieceDict[data] == (currentTurn, "P"):
                        legalMoves = chess.pawnMoves(currentTurn, data, pieceDict, lastMove, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "N"):
                        legalMoves = chess.knightMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "R"):
                        legalMoves = chess.rookMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "B"):
                        legalMoves = chess.bishopMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "Q"):
                        legalMoves = chess.queenMoves(currentTurn, data, pieceDict, kingPositions[currentTurn])

                    elif pieceDict[data] == (currentTurn, "K"):
                        legalMoves = chess.kingMoves(currentTurn, data, pieceDict, moveList)

                    #The user is sent necessary information, including the legalMoves he could make
                    conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )

                #If the client is selecting a piece to move
                else:

                    #Determines whether the move is legal by checking whether the move exists in the list of potential legalMoves
                    legal = False
                    for potMove in legalMoves[1:]:

                        #If the coordinate sent is in the list of potential moves
                        if data == potMove[:2]:

                            #If the move has special conditions, it records them
                            if len( potMove ) == 3:
                                special = potMove[2]
                            else:
                                special = None

                            #It sets the move as being legal, and exits the loop
                            legal = True
                            break

                    #If the move is legal
                    if legal:
                        
                        #Adds the last move to the moveList
                        moveList.append( [ legalMoves[0], pieceDict[ legalMoves[0] ], data, pieceDict[ data ], special ] )

                        #Changes king pos
                        if pieceDict[legalMoves[0]][1] == "K":
                            kingPositions[currentTurn] = data

                        #En passant
                        if special == "ep" and currentTurn == WHITE:
                            pieceDict[ (data[0], data[1] + 1) ] = None

                        elif special == "ep" and currentTurn == BLACK:
                            pieceDict[ (data[0], data[1] - 1) ] = None

                        #King side Castling
                        elif special == "O-O":
                            pieceDict[ (data[0] - 1, data[1] ) ] = (currentTurn, "R")
                            pieceDict[ (7, data[1]) ] = None

                        #Queen side castling
                        elif special == "O-O-O":
                            pieceDict[ (data[0] + 1, data[1]) ] = (currentTurn, "R")
                            pieceDict[ (0, data[1]) ] = None

                        #Pawn promotion
                        if pieceDict[ data ] == (WHITE, "P") and data[1] == 0:
                            pieceDict[ data ] = (WHITE, "Q")

                        elif pieceDict[ data ] == (BLACK, "P") and data[1] == 7:
                            pieceDict[ data ] = (BLACK, "Q")
                        

                        #Changes the player's turn
                        if currentTurn == WHITE:
                            currentTurn = BLACK
                        else:
                            currentTurn = WHITE

                        #If the opponent's king is in check as a result of the move
                        if not chess.inCheck(legalMoves[0], data[:2], pieceDict, kingPositions[currentTurn], currentTurn):

                            #Modifies the pieceDict to perform the legal move
                            pieceDict[ data[:2] ] = pieceDict[ legalMoves[0] ]
                            pieceDict[ legalMoves[0] ] = None

                            #Determines whether the opponent can make any legal moves
                            checkmate = True

                            #For every piece in the board that is the opponent's colour, it checks whether it can make a move if it can it sets checkmate to false
                            for coord, piece in pieceDict.items():
                                if piece != None and piece[0] == currentTurn:
                                    if pieceDict[ coord ][1] == "P" and len( chess.pawnMoves(currentTurn, coord, pieceDict, lastMove, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "N" and len( chess.knightMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "R" and len( chess.rookMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "B" and len( chess.bishopMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "Q" and len( chess.queenMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        checkmate = False
                                        break

                                    elif pieceDict[ coord ][1] == "K" and len( chess.kingMoves(currentTurn, coord, pieceDict, moveList) ) > 1:
                                        checkmate = False
                                        break

                            #If the user can make no legal moves it adds checkmate to the end of the moveList's last move
                            if checkmate:
                                moveList[-1].append("checkmate")

                            #Otherwise, it adds check to the end of the moveList's last move
                            else:
                                moveList[-1].append("check")

                        #If the opponent's king is not in check
                        else:

                            #Moves the chess piece to its new tile
                            pieceDict[ data[:2] ] = pieceDict[ legalMoves[0] ]
                            pieceDict[ legalMoves[0] ] = None

                            #Determines whether the opponent can make any legal moves
                            stalemate = True

                            #For every piece in the board that is the opponent's colour, it checks whether it can make a move if it can it sets checkmate to false
                            for coord, piece in pieceDict.items():
                                if piece != None and piece[0] == currentTurn:
                                    if pieceDict[ coord ][1] == "P" and len( chess.pawnMoves(currentTurn, coord, pieceDict, lastMove, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "N" and len( chess.knightMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "R" and len( chess.rookMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "B" and len( chess.bishopMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "Q" and len( chess.queenMoves(currentTurn, coord, pieceDict, kingPositions[currentTurn]) ) > 1:
                                        stalemate = False
                                        break

                                    elif pieceDict[ coord ][1] == "K" and len( chess.kingMoves(currentTurn, coord, pieceDict, moveList) ) > 1:
                                        stalemate = False
                                        break

                            #If the user can make no legal moves it adds stalemate to the end of the moveList's last move
                            if stalemate:
                                moveList[-1].append("stalemate")

                            #Otherwise, it adds None to the end of the moveList's last move
                            else:
                                moveList[-1].append(None)

                        #Sets the lastMove equal to the last item in the moveList
                        #The lastMove is utilised to determine the correct notation for that move
                        lastMove = moveList[-1]

                        #THE CODE BELOW DETERMINES THE CORRECT NOTATION TO FOR THE LAST MOVE AND ADDS IT TO THE MOVE NOTATION LIST

                        #If the lastMove is king side castling
                        if lastMove[4] == "O-O":
                            if lastMove[5] == None:
                                moveNotation.append("O-O")

                            if lastMove[5] == "check":
                                moveNotation.append("O-O+")

                            elif lastMove[5] == "checkmate":
                                moveNotation.append("O-O#")

                            elif lastMove[5] == "stalemate":
                                moveNotation.append("O-O1/2")

                        #If the lastMove is queen side castling
                        elif lastMove[4] == "O-O-O":

                            if lastMove[5] == None:
                                moveNotation.append("O-O-O")

                            if lastMove[5] == "check":
                                moveNotation.append("O-O-O+")

                            elif lastMove[5] == "checkmate":
                                moveNotation.append("O-O-O#")

                            elif lastMove[5] == "stalemate":
                                moveNotation.append("O-O-O1/2")

                        #Otherwise
                        else:

                            #Puts the move into the notation [Starting Coordinate][Piece Used][Adds an "x" if the move involved taking another piece][Ending Coordinate]
                            #The coordinates are in the form letter than number (ex. e4)
                            notation = Num2Letter[ lastMove[0][0] ] + str(lastMove[0][1] + 1) + lastMove[1][1]
                            
                            if lastMove[3] != None:
                                notation += "x"
                                
                            notation += Num2Letter[ lastMove[2][0] ] + str(lastMove[2][1] + 1)
                            
                            if lastMove[4] == "ep":
                                notation += "e.p."

                            if lastMove[5] == "check":
                                notation += "+"

                            elif lastMove[5] == "checkmate":
                                notation += "#"

                            elif lastMove[5] == "stalemate":
                                notation += "1/2"

                            moveNotation.append( notation )

                        #Sets the alertMsg to None, and sets the legalMoves to an empty list
                        alertMsg = None; legalMoves = list()

                        #Returns necessary information back to the client
                        conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )

                    #Otherwise, the move was not legal
                    else:
                        
                        #Sets the legalMoves to an empty list
                        legalMoves = list()

                        #Returns necessary information back to the client
                        conn.sendall( pickle.dumps( (alertMsg, legalMoves, pieceDict, moveNotation) ) )

            #Otherwise, it was not the user's turn            
            else:
                
                #Sends the user a message that it was not their turn
                conn.sendall( pickle.dumps("Wrong Turn") )
        
        except:
            break

    #If the user has lost connection in closes the socket
    print("Lost connection to", currentPlayer)
    conn.close()
        

currentPlayer = WHITE
while 1:
    conn, addr = s.accept()
    print ("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = BLACK
