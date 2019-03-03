import re


def talkToArduino(orig_col, orig_row, new_col, new_row, piece_type, capture):  # need to tell arduino start position, end position, piece type and if it is a removal or not.
    # send the info to the arduino.
    print("SaH duino")



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
    print("checking move")

    if orig_col<0 or orig_row<0 or new_col<0 or new_row<0 or orig_col>7 or orig_row>7 or new_col>7 or new_row>7:
        print("Invalid Move! Board location does not exist. Please repeat")

    piece = game.getitem(orig_col, orig_row)
    print(piece.colour, piece.type)

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


while True:
    game_loop()
