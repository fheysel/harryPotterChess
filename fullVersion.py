import re
from nanpy import (ArduinoApi, SerialManager)
from time import sleep

currentX = 0
currentY = 0

list[1, 2, 3]

def step(dir, dirPin, stepperPin, steps):
    delayTime = 0.00008
    if dirPin == 7: # set faster for z motion
        delayTime = 0.00003

    duino.digitalWrite(dirPin, dir)
    sleep(0.1)

    for x in range(steps):
        duino.digitalWrite(stepperPin, duino.HIGH)
        sleep(delayTime)
        duino.digitalWrite(stepperPin, duino.LOW)
        sleep(delayTime)

def stepDiagonally(dir1, dirPin1, stepperPin1, dir2, dirPin2, stepperPin2, steps):
    delayTime = 0.00008

    duino.digitalWrite(dirPin1, dir1)
    duino.digitalWrite(dirPin2, dir2)
    sleep(0.1)

    for x in range(steps):
        duino.digitalWrite(stepperPin1, duino.HIGH)
        duino.digitalWrite(stepperPin2, duino.HIGH)
        sleep(delayTime)
        duino.digitalWrite(stepperPin1, duino.LOW)
        duino.digitalWrite(stepperPin2, duino.LOW)
        sleep(delayTime)

def magnet(state):
    step(state, Z_DIR_PIN, Z_STP_PIN, 6400*0.25) # move the z axis a quarter revolution to turn on or off


def talkToArduino(orig_col, orig_row, new_col, new_row, piece_type, capture):  # need to tell arduino start position, end position, piece type and if it is a removal or not.

    origCol = orig_col + 1 # converting the 10X10 grid
    origRow = orig_row + 1
    newCol = new_col + 1
    newRow = new_row + 1

    if capture is True:
        moveArm(newCol, newRow, 0)
        magnet(1) # magnet on
        nearestWall = findNearestWall(newCol, newRow)
        if nearestWall == 'bottom':
            wallPosCol = newCol + x_offset
            wallPosRow = 0
            order = 0 # y first
        elif nearestWall == 'top':
            wallPosCol = newCol + x_offset
            wallPosRow = 9
            order = 0 # y first
        elif nearestWall == 'left':
            wallPosCol = 0
            wallPosRow = newRow + y_offset
            order = 1 # x first
        else:
            wallPosCol = 9
            wallPosRow = newRow + y_offset
            order = 1 # x first
        moveArm(wallPosCol, wallPosRow, order)
        magnet(0)
    else:
        moveArm(origCol, origRow, 0)
        magnet(1)
        if origCol != newCol and origRow != newRow and piece_type != "knight":
            order = 2 # indicates diagonal movement of arm
        elif piecetype == "knight":
            order = 3 # indicates knight move
        else:
            order = 1 # order doesnt matter as there will only be movement in one arm. 1 was chosen arbritarily, could have been 0.

        moveArm(newCol, newRow, order)
        magnet(0)


def moveArm(newCol, newRow, order):
    tileStep = 4800 # steps per one tile

    amountToMoveX = newRow - currentX
    amountToMoveY = newCol - currentY

    if amountToMoveX < 0 :
        xDir = False # move x counter clockwise
        amountToMoveX = abs(amountToMoveX)
    else:
        xDir = True
    if amountToMoveY < 0 :
        yDir = False # move y counter clockwise

        amountToMoveY = abs(amountToMoveY)
    else:
        yDir = True

    if order == 0 :
        step(yDir, Y_DIR_PIN, Y_STP_PIN, amountToMoveY) # move y axis
        step(xDir, X_DIR_PIN, X_STP_PIN, amountToMoveX)# move x axis
    elif order == 1 :
        step(xDir, X_DIR_PIN, X_STP_PIN, amountToMoveX)  # move x axis
        step(yDir, Y_DIR_PIN, Y_STP_PIN, amountToMoveY)  # move y axis
    elif order == 2 :
        stepDiagonally(xDir, X_DIR_PIN, X_STP_PIN, yDir, Y_DIR_PIN, Y_STP_PIN, amountToMoveY)# move both at same time. amountToMoveY was used arbritatrily, could have been X
    else :
        if newRow > currentX: # knight moves up
            yDir = True
        else:
            yDir = False
        if newCol > currentY:  # knight moves left
            xDir = True
        else:
            xDir = False

        if abs(newRow - currentX) == 2:  # Long L shape
            step(xDir, X_DIR_PIN, X_STP_PIN, 0.5*tileStep)# move half tile on x axis
            step(yDir, Y_DIR_PIN, Y_STP_PIN, 2*tileStep) # move two tiles on y axia
            step(xDir, X_DIR_PIN, X_STP_PIN, 0.5 * tileStep) # move half tile on x axis
        else:
            step(yDir, Y_DIR_PIN, Y_STP_PIN, 0.5 * tileStep) # move half tile on y axis
            step(xDir, X_DIR_PIN, X_STP_PIN, 2 * tileStep) # move two tiles on x axis
            step(yDir, Y_DIR_PIN, Y_STP_PIN, 0.5 * tileStep)  # move half tile on y axis



def findNearestWall(newCol, newRow):
    bottomDis = newRow;
    leftDis = newCol;
    rightDis = 7 - leftDis;
    topDis = 7 - bottomDis;

    shortestVertDis = min(bottomDis, topDis);
    shortestHorDis = min(leftDis, rightDis);

    shortestDis = min(shortestVertDis, shortestHorDis);

    if (shortestDis == bottomDis):
        return "bottom";
    elif (shortestDis == topDis):
        return "top"
    elif (shortestDis == "leftDis"):
        return "left"
    else:
        return "right"


class Piece:
    def __init__(self, type, colour):
        self.type = type
        self.colour = colour


class Board:
    # board pieces
    wpawn = Piece('pawn', 'white')
    wrook = Piece('rook', 'white')
    wknight = Piece('knight', 'white')
    wbishop = Piece('bishop', 'white')
    wqueen = Piece('queen', 'white')
    wking = Piece('king', 'white')

    bpawn = Piece('pawn', 'black')
    brook = Piece('rook', 'black')
    bknight = Piece('knight', 'black')
    bbishop = Piece('bishop', 'black')
    bqueen = Piece('queen', 'black')
    bking = Piece('king', 'black')

    # Creating columns on board
    a = list()
    a.append(wrook)
    a.append(wpawn)
    for i in range(0, 4):
        a.append(None)
    a.append(bpawn)
    a.append(brook)

    b = list()
    b.append(wknight)
    b.append(wpawn)
    for i in range(0, 4):
        b.append(None)
    b.append(bpawn)
    b.append(bknight)

    c = list()
    c.append(wbishop)
    c.append(wpawn)
    for i in range(0, 4):
        c.append(None)
    c.append(bpawn)
    c.append(bbishop)

    d = list()
    d.append(wqueen)
    d.append(wpawn)
    for i in range(0, 4):
        d.append(None)
    d.append(bpawn)
    d.append(bqueen)

    e = list()
    e.append(wking)
    e.append(wpawn)
    for i in range(0, 4):
        e.append(None)
    e.append(bpawn)
    e.append(bking)

    f = list()
    f.append(wbishop)
    f.append(wpawn)
    for i in range(0, 4):
        f.append(None)
    f.append(bpawn)
    f.append(bbishop)

    g = list()
    g.append(wknight)
    g.append(wpawn)
    for i in range(0, 4):
        g.append(None)
    g.append(bpawn)
    g.append(bknight)

    h = list()
    h.append(wrook)
    h.append(wpawn)
    for i in range(0, 4):
        h.append(None)
    h.append(bpawn)
    h.append(brook)

    board = list()
    board.append(a)
    board.append(b)
    board.append(c)
    board.append(d)
    board.append(e)
    board.append(f)
    board.append(g)
    board.append(h)

    checkmate = False

    def get_full_name(self, col, row):
        piece = self.board[col][row]
        if piece is None:
            colour = "no"
            type = "piece"
        else:
            colour = piece.colour
            type = piece.type
        return colour+" "+type

    def print_board(self):
        for j in range(0, 8):
            for i in range(0, 8):
                name = self.get_full_name(i, j)
                print('{:20}'.format(name), end=" ")
            print('')

    def getitem(self, i, j):
        return self.board[i][j]

    def setitem(self, i, j, piece):
        self.board[i][j] = piece

    def __init__(self):
        self.print_board()


def capture(piece, game, orig_col, orig_row, new_col, new_row):
    dead_piece = game.board[new_col][new_row]
    talkToArduino(orig_col, orig_row, new_col, new_row, piece.type, 1)
    print("capturing ", dead_piece.colour, " ", dead_piece.type)
    if dead_piece.type == "king":
        if dead_piece.colour == "white":
            print("CONGRATULATIONS BLACK!")
        else:
            print("CONGRATULATIONS WHITE!")

        game.checkmate = True


def translate_move(move):
    if move == "exit":
        quit()

    regex = re.compile(r'[a-hA-H][0-7] ?to ?[a-hA-H][0-7]')
    if regex.search(move) is None:
        return -1, -1, -1, -1

    parsed_move = move.split("to")

    original_pos = parsed_move[0]
    new_pos = parsed_move[1]
    original_pos = original_pos.strip()  # gets rid of trailing space
    new_pos = new_pos.strip()  # gets rid of leading space

    original_column = ord(original_pos[0].upper()) - 65  # converts the column letter to the appropriate number
    original_row = original_pos[1]
    new_column = ord(new_pos[0].upper()) - 65
    new_row = new_pos[1]

    return int(original_column), int(original_row), int(new_column), int(new_row)


def check_move(orig_col, orig_row, new_col, new_row, game):
    if orig_col<0 or orig_row<0 or new_col<0 or new_row<0 or orig_col>7 or orig_row>7 or new_col>7 or new_row>7:
        print("Invalid Move! Board location does not exist. Please repeat")

    piece = game.getitem(orig_col, orig_row)

    valid_move = False
    if piece.type == "pawn":
        valid_move = check_pawn(piece, game, orig_col, orig_row, new_col, new_row)
    elif piece.type == "rook":
        valid_move = check_rook(piece, game, orig_col, orig_row, new_col, new_row)
    elif piece.type == "knight":
        valid_move = check_knight(piece, game, orig_col, orig_row, new_col, new_row)
    elif piece.type == "bishop":
        valid_move = check_bishop(piece, game, orig_col, orig_row, new_col, new_row)
    elif piece.type == "queen":
        valid_move = check_queen(piece, game, orig_col, orig_row, new_col, new_row)
    elif piece.type == "king":
        valid_move = check_king(piece, game, orig_col, orig_row, new_col, new_row)
    else:
        print("Invalid piece??? Probs a typo in the code")

    return valid_move


def check_promotion(piece, game, new_row, new_col):
    if piece.colour == "white" and new_row == 7:
        piece.type = "queen"
        game.setitem(new_row, new_col, piece)
    elif piece.colour == "black" and new_row == 0:
        piece.type = "queen"
        game.setitem(new_row, new_col, piece)


def check_pawn(piece, game, orig_col, orig_row, new_col, new_row):
    other_piece = game.getitem(new_col, new_row)

    # check correct direction
    if piece.colour == "white" and orig_row > new_row:
        return False
    elif piece.colour == "black" and orig_row < new_row:
        return False

    # check if valid capture
    if orig_col != new_col:
        if abs(orig_row - new_row) != 1 and abs(orig_col - new_col) != 1:  # not one diagonal spot away
            return False
        else:
            if other_piece is None or other_piece.colour == piece.colour:
                return False
            else:
                capture(piece, game, orig_col, orig_row, new_col, new_row)
                check_promotion(piece, game, new_row, new_col)
                return True

    # else moving forward
    if abs(orig_row - new_row) == 1:
        if game.getitem(orig_col, orig_row+1) is None and piece.colour == "white":  # if nothing one spot ahead
            check_promotion(piece, game, new_row, new_col)
            return True
        elif game.getitem(orig_col, orig_row-1) is None and piece.colour == "black":
            check_promotion(piece, game, new_row, new_col)
            return True
        else:
            return False

    # check if valid first double jump
    elif abs(orig_row - new_row) == 2:
        if orig_row == 1 and game.getitem(orig_col, orig_row+1) is None and game.getitem(orig_col, orig_row+2) is None\
                and piece.colour == "white":  # if nothing one or two spots ahead
            return True
        elif orig_row == 6 and game.getitem(orig_col, orig_row-1) is None and game.getitem(orig_col, orig_row-2) is None\
                and piece.colour == "black":
            return True
        else:
            return False

    else:
        return False


def check_rook(piece, game, orig_col, orig_row, new_col, new_row):
    # check if straight line
    if orig_col != new_col and orig_row != new_row:
        return False

    else:  # check if path is clear
        if orig_row < new_row:  # going up
            row_incrementor = 1
            col_incrementor = 0
        elif orig_row > new_row:  # going down
            row_incrementor = -1
            col_incrementor = 0
        elif orig_col < new_col:  # going right
            row_incrementor = 0
            col_incrementor = 1
        else:  # going left
            row_incrementor = 0
            col_incrementor = -1

        return check_path(piece, game, orig_col, orig_row, new_col, new_row, col_incrementor, row_incrementor)


def check_bishop(piece, game, orig_col, orig_row, new_col, new_row):
    if abs(orig_row - new_row) != abs(orig_col - new_col):
        return False
    else:  # check if path is clear
        if orig_row < new_row and orig_col < new_col:  # going up and to the right
            row_incrementor = 1
            col_incrementor = 1
        elif orig_row < new_row and orig_col > new_col:  # going up and to the left
            row_incrementor = 1
            col_incrementor = -1
        elif orig_row > new_row and orig_col < new_col:  # going down and to the right
            row_incrementor = -1
            col_incrementor = 1
        else:  # going down and to the left
            row_incrementor = -1
            col_incrementor = -1

        return check_path(piece, game,orig_col, orig_row, new_col, new_row, col_incrementor, row_incrementor)


def check_knight(piece, game, orig_col, orig_row, new_col, new_row):
    other_piece = game.board[new_col][new_row]
    if abs(orig_row - new_row) == 2 and abs(orig_col - new_col) == 1:#up two across one
        if other_piece is None:
            return True
        else:
            if other_piece.colour != piece.colour:
                capture(piece, game, orig_col, orig_row, new_col, new_row)
                return True
            else:
                return False
    elif abs(orig_row - new_row) == 1 and abs(orig_col - new_col) == 2:#up one across two
        if other_piece is None:
            return True
        else:
            if other_piece.colour != piece.colour:
                capture(piece, game, orig_col, orig_row, new_col, new_row)
                return True
            else:
                return False
    else:
        return False


def check_king(piece, game, orig_col, orig_row, new_col, new_row):
    if abs(orig_col - new_col) <= 1 and abs(orig_row - new_row) <=1:
        return check_queen(piece, game,orig_col, orig_row, new_col, new_row)
    else:
        return False


def check_queen(piece, game, orig_col, orig_row, new_col, new_row):
    if check_bishop(piece, game, orig_col, orig_row, new_col, new_row) or check_rook(piece, game, orig_col, orig_row,
                                                                                     new_col, new_row):
        return True
    else:
        return False


def check_path(piece, game, orig_col, orig_row, new_col, new_row, col_incrementor, row_incrementor):
    temp_col = orig_col + col_incrementor
    temp_row = orig_row + row_incrementor

    while temp_col != new_col:  # could do by row but doesn't really matter
        if game.board[temp_col][temp_row] is not None:
            return False
        temp_row += row_incrementor
        temp_col += col_incrementor

    if game.board[new_col][new_row] is None:
        return True
    elif game.board[new_col][new_row].colour != piece.colour:
        capture(piece, game, orig_col, orig_row, new_col, new_row)
        return True
    else:
        return False


def game_loop():
    game = Board()
    turn = 0  # one represents white 1 represents black

    while game.checkmate is not True:
        valid_move = False
        while not valid_move:
            move = input("What is your move?")
            orig_col, orig_row, new_col, new_row = translate_move(move)

            if orig_col == -1 or orig_row == -1 or new_col == -1 or new_row == -1:
                print("Invalid input, please try again")
            else:
                piece = game.getitem(orig_col, orig_row)
                if piece is None:
                    print("Invalid Move! No piece at the location. Please repeat")
                else:
                    if game.board[orig_col][orig_row].colour == "white" and turn == 0 or game.board[orig_col][orig_row].colour == "black" and turn == 1:
                        valid_move = check_move(orig_col, orig_row, new_col, new_row, game)
                    else:
                        print("Not your turn")

                    if not valid_move:
                        print("Invalid move", move, ". Try again.")

        print("Your move ", move, " is valid")
        turn = turn ^ 1

        # UPDATE BOARD
        talkToArduino(orig_col, orig_row, new_col, new_row, game.board[orig_col][orig_row].type, 0)
        game.setitem(new_col, new_row, game.board[orig_col][orig_row])
        game.setitem(orig_col, orig_row, None)
        game.print_board()


#START WITH ARDUINO SETUP
# set up setial connection
EN = 8
X_DIR_PIN = 5
Y_DIR_PIN = 6
Z_DIR_PIN = 7

X_STP_PIN = 2
Y_STP_PIN = 3
Z_STP_PIN = 4

delayTime = 30 #Delay between each pause (uS)
stps = 6400 # steps in one revolution

try:
    connection = SerialManager()
    duino = ArduinoApi(connection = connection)

    #VOID SETUP
    duino.pinMode(X_DIR_PIN, duino.OUTPUT)
    duino.pinMode(X_STP_PIN, duino.OUTPUT)

    duino.pinMode(Y_DIR_PIN, duino.OUTPUT)
    duino.pinMode(Y_STP_PIN, duino.OUTPUT)

    duino.pinMode(Z_DIR_PIN, duino.OUTPUT)
    duino.pinMode(Z_STP_PIN, duino.OUTPUT)

    duino.pinMode(EN, duino.OUTPUT)
    duino.digitalWrite(EN, duino.LOW)


    while True:
        game_loop()

except:
    print("Connection to Arduino failed")
