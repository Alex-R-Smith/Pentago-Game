''' Alex Smith 5/5/2017 PA #2 '''

import sys, re
from copy import deepcopy  


#board = [str(x).zfill(2) for x in range(36)]
board = ['.' for x in range(36)]
indices1 = [0,1,2,6,7,8,12,13,14]
indices2 = [3,4,5,9,10,11,15,16,17]
indices3 = [18,19,20,24,25,26,30,31,32]
indices4 = [21,22,23,27,28,29,33,34,35]
p1Name = ''
computer = 'COMPUTER'
p1Token = ''
cpToken = ''
depthlimit = 2
deltadepth = 0

#helper globals
rows = ((0,1,2,3,4,5),(6,7,8,9,10,11),(12,13,14,15,16,17),
          (18,19,20,21,22,23),(24,25,26,27,28,29),(30,31,32,33,34,35))
columns = ((0,6,12,18,24,30),(1,7,13,19,25,31),(2,8,14,20,26,32),
              (3,9,15,21,27,33),(4,10,16,22,28,34),(5,11,17,23,2,9,35))
rightDiag = ((24,31),(18,25,32),(12,19,26,33),(6,13,20,27,33),(0,7,14,21,28,35),
                 (1,8,15,22,29),(2,9,16,23),(3,10,17),(04,11))
leftDiag = ((29,34),(23,28,33),(17,22,27,32),(11,16,21,26,31),(5,10,15,20,25,30),
                (4,9,14,19,24),(3,8,13,18),(2,7,12),(1,6))
lines = (rows + columns + rightDiag + leftDiag)
fileout = open('Output.txt', 'w')


# creates the gameNode class used to store the states of the game board
class gameNode:
        
        state = None
        value = 0
        depth = 0
        children = []
        lastmove = ''
        
        #gets all of the children for a state
        def getChildren(self, token):
            moves = possibleMoves(self.state)
            for move in moves:
                child = gameNode()
                child.state = deepcopy(self.state)
                child.lastmove = move
                child.depth = self.depth + 1
                child.children = []
                child.value = 0
                doMove(move, child.state, token)
                exists = False
                for existing in self.children:
                    if child.state == existing.state:
                        exists = True
                        break
                if not exists:
                    self.children.append(child)


        #print override that prints game boards with depth tabs
        def __str__(self):
            output = ""
            self.depth
            output += "".join(['\t']*self.depth)
            output += "".join(self.state) + '\n'
            for child in self.children:
                output += str(child) 
            return output
        

#AI class - holds the AI for both minimax and alphabeta
class AI:
    
    root = gameNode()
    currentNode = None
    nodeExpanded = 0
    #AI Computers move
    def com_move(self, board, computer, cpToken, p1Name, p1Token, searchmethod):

        self.root.state = board
        self.root.depth = 0
        self.root.lastmove = ''
        self.root.children = []
        self.root.value = 0
        self.currentNode = self.root
        move = None
        if searchmethod == 'MiniMax':
            move = self.minimax(self.currentNode)
        else:
            move = self.alphaBeta(self.currentNode)  
        self.currentNode = None
        # print move
        return move.lastmove
    
    #minimax funciton call to do the minimax algorithm
    def minimax(self, node):
        global depthlimit
        if len(node.children) == 0:
            node.getChildren(cpToken)
        depthlimit += deltadepth
        best_val = self.max_value(node)
        node.value = best_val
        best_move = None
        for child in node.children:
            if child.value == best_val:
                best_move = child
                break
        return best_move


    #max Value calculation
    def max_value(self, node):
        if node.depth < depthlimit:
            if len(node.children) == 0:
                node.getChildren(cpToken)
        if self.isLeaf(node):
            return utility(node.state, p1Token, cpToken)

        infinity = float('inf')
        max_value = -infinity
        for child in node.children:
            child.value = self.min_value(child)
            max_value = max(max_value, child.value)
        return max_value

    #min value calculation
    def min_value(self, node):
        if node.depth < depthlimit:
            if len(node.children) == 0:
                node.getChildren(p1Token)

        if self.isLeaf(node):
            return utility(node.state, cpToken, p1Token)

        infinity = float('inf')
        min_value = infinity
        for child in node.children:
            child.value = self.max_value(child)
            min_value = min(min_value, child.value)  
        return min_value
    
    
    #alpha beta algorithm
    def alphaBeta(self, node):
        global depthlimit
        if len(node.children) == 0:
            node.getChildren(cpToken)
            self.nodeExpanded += 1
        beta = float('inf')
        alpha = -float('inf')
        depthlimit += deltadepth
        for child in node.children:
            child.value = self.ab_min_value(child, alpha, beta)
            if child.value > alpha:
                alpha = child.value
                best_move = child
        return best_move


    #max Value calculation
    def ab_max_value(self, node, alpha, beta):
        if node.depth < depthlimit:
            if len(node.children) == 0:
                node.getChildren(cpToken)
                self.nodeExpanded +=1
        if self.isLeaf(node):
            return utility(node.state, p1Token, cpToken)

        currentValue = -float('inf')

        for child in node.children:
            child.value = self.ab_min_value(child, alpha, beta)
            currentValue = max(currentValue, child.value)
            if currentValue >= beta:
                return currentValue
            alpha = max(alpha, currentValue)
        return currentValue

    #min value calculation
    def ab_min_value(self, node, alpha, beta):
        if node.depth < depthlimit:
            if len(node.children) == 0:
                node.getChildren(p1Token)
                self.nodeExpanded += 1
        if self.isLeaf(node):
            return utility(node.state, cpToken, p1Token)

        currentValue = float('inf')
        for child in node.children:
            child.value = self.ab_max_value(child, alpha, beta)
            currentValue = min(currentValue, child.value)
            if currentValue <= alpha:
                return currentValue
            beta = min(beta, currentValue)
        return currentValue

    #figures out if a node is a leaf or not
    def isLeaf(self, node):
        if node is not None:
            return len(node.children) == 0

# prints the game board all pretty
def printBoard(board):
    y = 0
    output = ''
    output +=  "\n+-------+-------+\n"
    for x in range(len(board)):
        if (x%3) == 0:
            if (x%6) == 0 and x != 0:
                output +=  '|\n'
                if (x%18) == 0:
                    output +=  "+-------+-------+\n"
            output += '| ' + board[y] + ' '
        else:
            output += board[y] + ' '
        y += 1
    output += '|\n'
    output += "+-------+-------+\n"
    return output

#board rotations
def rotateBoard(board, boardNumber, direction):
    if boardNumber == 1:
        board = dimReturn(board, rotateSection(dimUp([board[x] for x in indices1]), direction), boardNumber)
    elif boardNumber == 2:
        board = dimReturn(board, rotateSection(dimUp([board[x] for x in indices2]), direction), boardNumber)
    elif boardNumber == 3:
        board = dimReturn(board, rotateSection(dimUp([board[x] for x in indices3]), direction), boardNumber)
    elif boardNumber == 4:
        board = dimReturn(board, rotateSection(dimUp([board[x] for x in indices4]), direction), boardNumber)
    return board

#puts my single string board into a 2d array
def dimUp(board):
    board = [board[i:i+3] for i in range(0,len(board), 3)]
    return board

#returns the 2d array into my string
def dimReturn(board, twoDBoard, boardNumber):
    for y in range(3):
        for x in range(3):
            if boardNumber == 1:
                ind = indices1[x+3*y]
                board[ind] = twoDBoard[y][x]
            elif boardNumber == 2:
                ind = indices2[x+3*y]
                board[ind] = twoDBoard[y][x]
            elif boardNumber == 3:
                ind = indices3[x+3*y]
                board[ind] = twoDBoard[y][x]
            elif boardNumber == 4:
                ind = indices4[x+3*y]
                board[ind] = twoDBoard[y][x]
    return board

#rotates a quadrant of the board
def rotateSection(board, direction):
    if direction == 'L':
        rotated = zip(*board)[::-1]
    else:
        rotated = zip(*board[::-1])
    return rotated

#Opening input for general information like player name and which token.
def plr_input():
    global cpToken, p1Token, p1Name
    while True:
        plr1 = raw_input("Player 1 Name: ").upper()
        if not plr1.isalpha():
            print "Please enter letters only."
            continue
        else:
            break

    while True:
        p1Token = raw_input("Please pick B or W. ").upper()
        if p1Token not in ('B', 'W'):
            print "Please enter B or W. "
            continue
        else:
            break
    if p1Token == 'B':
        cpToken = 'W'
    else:
        cpToken = 'B'
    while True:
        first = raw_input("Please pick who goes first: B or W. ").upper()
        if p1Token not in ('B', 'W'):
            print "Please enter B or W for who goes first"
            continue
        else:
            break
    if first == 'B' and p1Token == 'B':
        first = plr1
    elif first == 'W' and p1Token == 'W':
        first = plr1
    else:
        first = computer
        
    return (plr1, p1Token, cpToken, first)


#error checking with a regular expression for move input
def turnInput(currentName):
    while True:
        print currentName, "enter turn command. "
        plr_turn = raw_input().upper()
        if not re.match("^[1-4]\/[1-9] [1-4][RL]", plr_turn):
            print "Error: Please enter your turn in the following format '3/8 4L'"
            continue
        else:
            break
    return plr_turn

#places a token on the board
def placement(board, boardNumber, space, token):
    if boardNumber == 1:
        boardReg = dimUp([board[x] for x in indices1])
        boardReg[(space-1)/3][(space-1)%3] = token
        board = dimReturn(board, boardReg, boardNumber)
    elif boardNumber == 2:
        boardReg = dimUp([board[x] for x in indices2])
        boardReg[(space-1)/3][(space-1)%3] = token
        board = dimReturn(board, boardReg, boardNumber)
    elif boardNumber == 3:
        boardReg = dimUp([board[x] for x in indices3])
        boardReg[(space-1)/3][(space-1)%3] = token
        board = dimReturn(board, boardReg, boardNumber)
    elif boardNumber == 4:
        boardReg = dimUp([board[x] for x in indices4])
        boardReg[(space-1)/3][(space-1)%3] = token
        board = dimReturn(board, boardReg, boardNumber)
    return


#checks the board for a win condition
def winCond(board):
    for i in range(36):
        if board[i] != '.':
            if i%6 < 2:
                if (board[i] == board[i+1] == board[i+2] == board[i+3] == board[i+4]):
                    return board[i]
            if i < 12:
                if (board[i] ==board[i+6] == board[i+12] == board[i+18] == board[i+24]):
                    return board[i]
            if (i%6 < 2) and (i < 12):
                if (board[i] == board[i+7] == board[i+14] == board[i+21] == board[i+28]):
                    return board[i]
            if (i%6 > 3) and (i < 12):
                if (board[i] == board[i+5] == board[i+10] == board[i+15] == board[i+20]):
                    return board[i]


#proclaims the winner of the game when the win condition has been met
def winner(win, p1Name, p1Token, computer, cpToken):
    if win:
        if win == p1Token:
            print printBoard(board)
            print "Game Over!", p1Name, "Wins the Game!"
            fileout.write("\nGame Over! " + p1Name + " Wins the Game!\n")
            sys.exit()
        if win == cpToken:
            print printBoard(board)
            print "Game Over!", computer, "wins the Game!"
            fileout.write("\nGame Over! " + computer + " Wins the Game!\n")
            sys.exit()
            
#tie case
def tie(board):
    if all(x != '.' for x in board):
        print 'The game is a tie'
        fileout.write('\nThe game is a tie')


#this does the players turn
def p_turn(board, p1Name, p1Token, computer, cpToken):
        while True:
            p1_turn = turnInput(p1Name)
            (reg, space, rotate, direction) = int(p1_turn[0]), int(p1_turn[2]), int(p1_turn[4]), p1_turn[5]
            if not avalMove(board, reg, space):
                print "Please input a valid move."
                continue
            else:
                break
        fileout.write(str(reg) + '/' + str(space) + ' ' + str(rotate) + direction)
        placement(board, reg, space, p1Token)
        winner(winCond(board), p1Name, p1Token, computer, cpToken)
        tie(board)
        rotateBoard(board, rotate, direction)
        print printBoard(board)
        fileout.write(printBoard(board))
        winner(winCond(board), p1Name, p1Token, computer, cpToken)
        tie(board)

# checks to see if a spot is availble for a token to be placed there
def avalMove(board, boardNumber, space):
    boardSpot = get_index(boardNumber, space-1)
    if board[boardSpot] == '.':
        return True
    else:
        return False

#makes a list of all possible moves
def possibleMoves(board):
    posMov = []
    for i in range(1,5):
        for j in range(1,10):
            for k in range(1,5):
                for d in ['L', 'R']:
                    if avalMove(board, int(i), int(j)):
                        posMov.append(str(i) + '/' + str(j) + ' ' + str(k) + d);
    return posMov

#helper function to grab the index of a board place from the string
def get_index(reg, move):
    if reg == 1:
        return indices1[move]
    elif reg == 2:
        return indices2[move]
    elif reg == 3:
        return indices3[move]
    elif reg == 4:
        return indices4[move]

#calculates the utility
#zero in a row = 0
#one in a row = +-5
#two in a row = +-25
#three in a row = +-125
#four in a row = +-625
#five or six in a row = +-3125
def utility(board, player, computer):
    value = 0
    seq = 0
    points = (0,5,25,125,625,3125,3125)
    for line in lines:
        for i in range(len(line)-1):
            if board[line[i]] == board[line[i+1]] and board[line[i]] != '.':
                seq += 1
            elif board[line[i]] != board[line[i+1]]:
                if board[line[i]] == computer:
                    value += points[seq]
                elif board[line[i]] == player:
                    value -= points[seq]
                seq = 0
        if seq != 0:
            if board[line[i]] == computer:
                value += points[seq]
            elif board[line[i]] == player:
                value -= points[seq]
            seq = 0
    return value

#does the move for AI
def doMove(move, board, token):
    reg = int(move[0])
    space = int(move[2])
    rotate = int(move[4])
    direction = move[5]
    placement(board, reg, space,token)
    rotateBoard(board, rotate, direction)
    

def main(argv):
    try:
        #enter either 'MiniMax' or AlphaBeta
        searchmethod = 'AlphaBeta'
        if searchmethod == 'MiniMax':
            Ai = AI()
        elif searchmethod == 'AlphaBeta':
            Ai = AI()
        (p1Name, p1Token, cpToken, first) = plr_input()
        print "\n", p1Name, p1Token, "\n", computer, cpToken, "\n", 'First Player: ', first
        fileout.write("\n"+ p1Name+ p1Token+ "\n"+ computer+ cpToken+ "\n" +'First Player: '+ first)
        print printBoard(board)
        fileout.write(printBoard(board))
        if p1Name == first: 
            while True:
                p_turn(board, p1Name, p1Token, computer, cpToken)
                move = Ai.com_move(board, computer, cpToken, p1Name, p1Token, searchmethod)
                fileout.write(move)
                (reg, space, rotate, direction) = int(move[0]), int(move[2]), int(move[4]), move[5]
                placement(board, reg, space, cpToken)
                winner(winCond(board), computer, cpToken, p1Name, p1Token)
                rotateBoard(board, rotate, direction)
                print printBoard(board)
                fileout.write(printBoard(board))
                winner(winCond(board), computer, cpToken, p1Name, p1Token)
        else:
            while True:
                move = Ai.com_move(board, computer, cpToken, p1Name, p1Token, searchmethod)
                fileout.write(move)
                (reg, space, rotate, direction) = int(move[0]), int(move[2]), int(move[4]), move[5]
                placement(board, reg, space, cpToken)
                winner(winCond(board), computer, cpToken, p1Name, p1Token)
                rotateBoard(board, rotate, direction)
                print printBoard(board)
                fileout.write(printBoard(board))
                winner(winCond(board), computer, cpToken, p1Name, p1Token)
                p_turn(board, p1Name, p1Token, computer, cpToken)
    finally:
        fileout.close()
if __name__ == "__main__":
    main(sys.argv[1:])

