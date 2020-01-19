# Name        :        Chess Piece Moves
# Author      :      Timmy Thorpe
# Description :     List of functions which return a list of legal moves for the various pieces

#Colours
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)

#All possible pawn moves
def pawnMoves(currentTurn, startPos, pieceDict, lastMove, kingPos):

    #List of legal moves
    legalMoves = list()
    legalMoves.append(startPos)

    #Checks whether the pawn moves up / down (depends on their colour)
    if currentTurn == WHITE:
        vertical = -1
    else:
        vertical = 1

    #En passant
    print(lastMove)
    if lastMove != None and lastMove[1][1] == "P" and abs( lastMove[2][1] - lastMove[0][1] ) == 2:

        if ( startPos[0] + 1, startPos[1] ) == lastMove[2]:
            if inCheck( startPos, (startPos[0] + 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
                legalMoves.append( ( startPos[0] + 1, startPos[1] + vertical, "ep") )

        elif ( startPos[0] - 1, startPos[1] ) == lastMove[2]:
            if inCheck( startPos, (startPos[0] - 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
                legalMoves.append( ( startPos[0] - 1, startPos[1] + vertical, "ep") )

    #Moving the pawn 1 or 2 spaces forward
    if pieceDict[ (startPos[0], startPos[1] + vertical) ] == None:

        #Moving the pawn 1 space forward
        if inCheck( startPos, (startPos[0], startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            legalMoves.append( (startPos[0], startPos[1] + vertical) )

        #Moving the pawn 2 spaces forward
        if inCheck( startPos, (startPos[0], startPos[1] + vertical * 2), pieceDict, kingPos, currentTurn ):

            if (vertical == 1 and startPos[1] == 1) or (vertical == -1 and startPos[1] == 6):

                if pieceDict[ (startPos[0], startPos[1] + 2 * vertical) ] == None:

                    legalMoves.append( (startPos[0], startPos[1] + 2 * vertical) )

    #Diagonal Moves
    try:
        if inCheck( startPos, (startPos[0] - 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            if pieceDict[ (startPos[0] - 1, startPos[1] + vertical) ] != None:
                if pieceDict[ startPos ][0] not in pieceDict[ (startPos[0] - 1, startPos[1] + vertical) ]:
                    legalMoves.append( (startPos[0] - 1, startPos[1] + vertical) )
    except:
        pass

    try:
        if inCheck( startPos, (startPos[0] + 1, startPos[1] + vertical), pieceDict, kingPos, currentTurn ):
            if pieceDict[ (startPos[0] + 1, startPos[1] + vertical) ] != None:
                if pieceDict[ startPos ][0] not in pieceDict[ (startPos[0] + 1, startPos[1] + vertical) ]:
                    legalMoves.append( (startPos[0] + 1, startPos[1] + vertical) )
    except:
        pass

    #Return's a list of legal moves
    return legalMoves

#Legal knight moves
def knightMoves(currentTurn, startPos, pieceDict, kingPos):

    #List of legal moves
    legalMoves = list()
    legalMoves.append(startPos)

    knightMoves = (
                  (startPos[0] + 1, startPos[1] + 2), (startPos[0] - 1, startPos[1] + 2),
                  (startPos[0] + 1, startPos[1] - 2), (startPos[0] - 1, startPos[1] - 2),
                  (startPos[0] + 2, startPos[1] + 1), (startPos[0] - 2, startPos[1] + 1),
                  (startPos[0] + 2, startPos[1] - 1), (startPos[0] - 2, startPos[1] - 1)
                  )

    for knightMove in knightMoves:
        try:
            if ( pieceDict[ knightMove ] == None or pieceDict[ knightMove ][0] != currentTurn ) and inCheck(startPos, knightMove, pieceDict, kingPos, currentTurn):
                legalMoves.append( knightMove )
        except:
            pass

    return legalMoves

#Rook moves
def rookMoves(currentTurn, startPos, pieceDict, kingPos):
    legalMoves = list()
    legalMoves.append(startPos)


    #Legal rook moves right
    for xPos in range(startPos[0] + 1, 8, 1):
        if pieceDict[ (xPos, startPos[1]) ] == None:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )

        elif pieceDict[ startPos ][0] != pieceDict[ (xPos, startPos[1]) ][0]:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )
                break

        else:
            break

    #Legal rook moves left
    for xPos in range(startPos[0] - 1, -1, -1):
        if pieceDict[ (xPos, startPos[1]) ] == None:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )

        elif pieceDict[ startPos ][0] != pieceDict[ (xPos, startPos[1]) ][0]:
            if inCheck(startPos, (xPos, startPos[1]), pieceDict, kingPos, currentTurn):
                legalMoves.append( (xPos, startPos[1]) )
                break

        else:
            break

    #Legal rook moves down
    for yPos in range(startPos[1] + 1, 8, 1):
        if pieceDict[ (startPos[0], yPos) ] == None:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )

        elif pieceDict[ startPos ][0] != pieceDict[ (startPos[0], yPos) ][0]:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )
                break

        else:
            break

    #Legal rook moves up
    for yPos in range(startPos[1] - 1, -1, -1):
        if pieceDict[ (startPos[0], yPos) ] == None:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )

        elif pieceDict[ startPos ][0] != pieceDict[ (startPos[0], yPos) ][0]:
            if inCheck(startPos, (startPos[0], yPos), pieceDict, kingPos, currentTurn):
                legalMoves.append( (startPos[0], yPos) )
                break

        else:
            break

    return legalMoves

#Bishop moves
def bishopMoves(currentTurn, startPos, pieceDict, kingPos):

    legalMoves = list()
    legalMoves.append(startPos)

    #Top right diagonal
    testCoordinate = (startPos[0] + 1, startPos[1] + 1)
    while testCoordinate in pieceDict.keys():

        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] + 1, testCoordinate[1] + 1)

    #Bottom right diagonal
    testCoordinate = (startPos[0] + 1, startPos[1] - 1)
    while testCoordinate in pieceDict.keys():

        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] + 1, testCoordinate[1] - 1)

    #Bottom left diagonal
    testCoordinate = (startPos[0] - 1, startPos[1] + 1)
    while testCoordinate in pieceDict.keys():
        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] - 1, testCoordinate[1] + 1)

    #Top left diagonal
    testCoordinate = (startPos[0] - 1, startPos[1] - 1)
    while testCoordinate in pieceDict.keys():
        if pieceDict[testCoordinate] == None:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)

        elif pieceDict[startPos][0] != pieceDict[testCoordinate][0]:
            if inCheck(startPos, testCoordinate, pieceDict, kingPos, currentTurn):
                legalMoves.append(testCoordinate)
                break

        else:
            break

        testCoordinate = (testCoordinate[0] - 1, testCoordinate[1] - 1)

    return legalMoves

#Queen moves
def queenMoves(currentTurn, startPos, pieceDict, kingPos):
    return rookMoves(currentTurn, startPos, pieceDict, kingPos) + bishopMoves(currentTurn, startPos, pieceDict, kingPos)[1:]

#King moves
def kingMoves(currentTurn, startPos, pieceDict, moveList):
    legalMoves = list()
    legalMoves.append(startPos)

    #Castling
    if currentTurn == WHITE:
        rank = 7
    else:
        rank = 0

    #If the past move did not put the king into check
    if len(moveList) > 0:
        if len(moveList[-1]) == 5 or moveList[-1][5] == None:

            #Checks whether king castling, or queen castling is possible
            kingCastle = True; queenCastle = True
            for move in moveList:
                if move[1] == (currentTurn, "K"):
                    kingCastle = False; queenCastle = False
                    break

                elif move[0] == (7, rank) or move[2] == (7, rank):
                    kingCastle = False

                elif move[0] == (0, rank) or move[2] == (0, rank):
                    queenCastle = False

            #King side castling
            if kingCastle and pieceDict[ (5, rank) ] == None and pieceDict[ (6, rank) ] == None:
                if inCheck(startPos, (5, rank), pieceDict, (5, rank), currentTurn) and inCheck(startPos, (6, rank), pieceDict, (6, rank), currentTurn):
                    legalMoves.append( (6, rank, "O-O") )

            #Queen side castling
            if queenCastle and pieceDict[ (3, rank) ] == None and pieceDict[ (2, rank) ] == None and pieceDict[ (1, rank) ] == None:

                if inCheck(startPos, (5, rank), pieceDict, (3, rank), currentTurn) and inCheck(startPos, (6, rank), pieceDict, (2, rank), currentTurn):
                    legalMoves.append( (2, rank, "O-O-O") )

    #Normal king moves
    kingMoves = (
                (startPos[0] - 1, startPos[1] - 1), (startPos[0], startPos[1] - 1),
                (startPos[0] + 1, startPos[1] - 1), (startPos[0] - 1, startPos[1]),
                (startPos[0] + 1, startPos[1]), (startPos[0] - 1, startPos[1] + 1),
                (startPos[0], startPos[1] + 1), (startPos[0] + 1, startPos[1] + 1)
                )

    #Adds the kingMove to legalMoves if it does not result in the king being in check, or result in the king exiting the chessboard
    for kingMove in kingMoves:
        try:
            if pieceDict[ kingMove ] == None or pieceDict[ kingMove ][0] != currentTurn:
                if inCheck(startPos, kingMove, pieceDict, kingMove, currentTurn):
                    legalMoves.append( kingMove )
        except:
            pass

    return legalMoves

#inCheck function which returns true if the king is not in check and false otherwise
#The inCheck function basically checks to see if any piece may take the king if a move is made
def inCheck(startPos, newPos, pieceDict, kingPos, currentTurn):

    potDict = dict(pieceDict)
    potDict[newPos] = potDict[startPos]; potDict[startPos] = None

    knightCoords = (
                   (kingPos[0] + 1, kingPos[1] + 2), (kingPos[0] - 1, kingPos[1] + 2),
                   (kingPos[0] + 1, kingPos[1] - 2), (kingPos[0] - 1, kingPos[1] - 2),
                   (kingPos[0] + 2, kingPos[1] + 1), (kingPos[0] - 2, kingPos[1] + 1),
                   (kingPos[0] + 2, kingPos[1] - 1), (kingPos[0] - 2, kingPos[1] - 1)
                   )

    for coord in knightCoords:
        if coord[0] > -1 and coord[0] < 8 and coord[0] > - 1 and coord[1] > -1 and coord[1] < 8:
            if potDict[coord] == None:
                pass

            elif potDict[coord][0] == currentTurn:
                pass

            elif potDict[coord][1] == "N":
                return False

    if kingPos[0] + 1 != 8:
        if potDict[ (kingPos[0] + 1, kingPos[1]) ] == None:

            for x in range(kingPos[0] + 1, 8):
                if potDict[(x, kingPos[1])] == None:
                    pass

                elif potDict[(x, kingPos[1])][0] == currentTurn:
                    break

                elif potDict[ (x, kingPos[1]) ][1] == "R" or potDict[ (x, kingPos[1]) ][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0] + 1, kingPos[1]) ][0] != currentTurn:
            if potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "R" or potDict[ (kingPos[0] + 1, kingPos[1]) ][1] == "Q":
                return False

    if kingPos[0] - 1 != -1:
        if potDict[ (kingPos[0] - 1, kingPos[1]) ] == None:

            for x in range(kingPos[0] - 1, -1, -1):
                if potDict[(x, kingPos[1])] == None:
                    pass

                elif potDict[(x, kingPos[1])][0] == currentTurn:
                    break

                elif potDict[(x, kingPos[1])][1] == "R" or potDict[ (x, kingPos[1]) ][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0] - 1, kingPos[1]) ][0] != currentTurn:
            if potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "K" or potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "R" or potDict[ (kingPos[0] - 1, kingPos[1]) ][1] == "Q":
                return False

    if kingPos[1] + 1 != 8:
        if potDict[ (kingPos[0], kingPos[1] + 1) ] == None:

            for y in range(kingPos[1] + 1, 8):
                if potDict[(kingPos[0], y)] == None:
                    pass

                elif potDict[(kingPos[0], y)][0] == currentTurn:
                    break

                elif potDict[(kingPos[0], y)][1] == "R" or potDict[(kingPos[0], y)][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0], kingPos[1] + 1) ][0] != currentTurn:
            if potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "K" or potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "R" or potDict[ (kingPos[0], kingPos[1] + 1) ][1] == "Q":
                return False

    if kingPos[1] - 1 != -1:
        if potDict[ (kingPos[0], kingPos[1] - 1) ] == None:

            for y in range(kingPos[1] - 2, -1, -1):
                if potDict[(kingPos[0], y)] == None:
                    pass

                elif potDict[(kingPos[0], y)][0] == currentTurn:
                    break

                elif potDict[(kingPos[0], y)][1] == "R" or potDict[(kingPos[0], y)][1] == "Q":
                    return False

                else:
                    break

        elif potDict[ (kingPos[0], kingPos[1] - 1) ][0] != currentTurn:
            if potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "R" or potDict[ (kingPos[0], kingPos[1] - 1) ][1] == "Q":
                return False

    if kingPos[0] + 1 < 8 and kingPos[1] + 1 < 8:
        if potDict[ (kingPos[0] + 1, kingPos[1] + 1) ] != None:
            if potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][0] != currentTurn and ( potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "P" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "B" or potDict[ (kingPos[0] + 1, kingPos[1] + 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] + num < 8 and kingPos[1] + num < 8:

                if potDict[ (kingPos[0] + num, kingPos[1] + num) ] == None:
                    pass

                elif potDict[ (kingPos[0] + num, kingPos[1] + num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] + num, kingPos[1] + num) ][1] == "B" or potDict[ (kingPos[0] + num, kingPos[1] + num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] + 1 < 8 and kingPos[1] - 1 > -1:
        if potDict[ (kingPos[0] + 1, kingPos[1] - 1) ] != None:
            if potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][0] != currentTurn and ( potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "P" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "B" or potDict[ (kingPos[0] + 1, kingPos[1] - 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] + num < 8 and kingPos[1] - num > -1:

                if potDict[ (kingPos[0] + num, kingPos[1] - num) ] == None:
                    pass

                elif potDict[ (kingPos[0] + num, kingPos[1] - num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] + num, kingPos[1] - num) ][1] == "B" or potDict[ (kingPos[0] + num, kingPos[1] - num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] - 1 > -1 and kingPos[1] + 1 < 8:
        if potDict[ (kingPos[0] - 1, kingPos[1] + 1) ] != None:
            if potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][0] != currentTurn and ( potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "P" or potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "K" or  potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "B" or potDict[ (kingPos[0] - 1, kingPos[1] + 1) ][1] == "Q"):
                return False

        else:
            num = 2
            while kingPos[0] - num > -1 and kingPos[1] + num < 8:

                if potDict[ (kingPos[0] - num, kingPos[1] + num) ] == None:
                    pass

                elif potDict[ (kingPos[0] - num, kingPos[1] + num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] - num, kingPos[1] + num) ][1] == "B" or potDict[ (kingPos[0] - num, kingPos[1] + num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    if kingPos[0] - 1 > -1 and kingPos[1] - 1 > -1:
        if potDict[ (kingPos[0] - 1, kingPos[1] - 1) ] != None:
            if potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][0] != currentTurn and ( potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "P" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "K" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "B" or potDict[ (kingPos[0] - 1, kingPos[1] - 1) ][1] == "Q"):
                return False
        else:
            num = 2
            while kingPos[0] - num > -1 and kingPos[1] - num > -1:

                if potDict[ (kingPos[0] - num, kingPos[1] - num) ] == None:
                    pass

                elif potDict[ (kingPos[0] - num, kingPos[1] - num) ][0] == currentTurn:
                    break

                elif potDict[ (kingPos[0] - num, kingPos[1] - num) ][1] == "B" or potDict[ (kingPos[0] - num, kingPos[1] - num) ][1] == "Q":
                    return False

                else:
                    break

                num += 1

    return True
