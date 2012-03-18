import copy

pieces = {'5W': [[1, 0], [2, 0], [0, 1], [1, 1], [0, 2]],                                 
          '5V': [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2]],                                 
          '5Y': [[0, 0], [1, 0], [2, 0], [3, 0], [1, 1]],                                 
          '5X': [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],                                  
          '5L': [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1]],                                 
          '5U': [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1]],                                 
          '5T': [[0, 0], [1, 0], [2, 0], [1, 1], [1, 2]],                                 
          '4T': [[0, 0], [1, 0], [2, 0], [1, 1]],                                         
          '3L': [[0, 0], [1, 0], [0, 1]],                                                 
          '3I': [[0, 0], [1, 0], [2, 0]],                                                 
          '4S': [[1, 0], [2, 0], [0, 1], [1, 1]],                                         
          '4O': [[0, 0], [1, 0], [0, 1], [1, 1]],                                         
          '4L': [[0, 0], [1, 0], [2, 0], [0, 1]],                                         
          '5N': [[0, 0], [1, 0], [1, 1], [2, 1], [3, 1]],                                 
          '5I': [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],                                 
          '4I': [[0, 0], [1, 0], [2, 0], [3, 0]],                                         
          '5Z': [[0, 0], [1, 0], [1, 1], [1, 2], [2, 2]],                                 
          '5F': [[1, 0], [2, 0], [0, 1], [1, 1], [1, 2]],                                 
          '5P': [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1]],                                 
          '2I': [[0, 0], [1, 0]],                                                         
          '1O': [[0, 0]]}
          
class Game():
    def place(self, player, tiles):
        """ Expects a player number and an array of [x,y] locations for tiles """
        for tile in tiles:
            x, y = tile
            self.board[x][y] = player
            
    def __init__(self):
        self.board = [[0 for i in range(20)] for j in range(20)]
        self.turn = 0
        self.players = { i: pieces.keys() for i in range(4) }
        print self.players
        self.start_corners = [[0,0], [19,0], [19,19], [0,19]]
        self.curr_turn = 1
        
    def hasPiece(self, player, key):
        if (self.players[player-1].count(key) == 0):
            return False
        return True
    
    def play(self, player, piece, rotations, flipped, location):
#        if (self.players[player+1].index(piece) != -1):
#            return False
        p = translatePiece(piece, rotations, flipped, location)
        corner = False
        
        for tile in p:
            x,y = tile
            if (x < 0 or x >= len(self.board) or y < 0 or y >= len(self.board[0]) or self.board[x][y] != 0):
                print "Overlap or out of bounds"
                return False
            for i,j in [[-1,0],[0,1],[1,0],[0,-1]]:
#                print x+i,y+j
                if (x+i < 0 or x+i >= len(self.board) or y+j < 0 or y+j >= len(self.board[0])):
                    pass
                elif (self.board[x+i][y+j] == player):
                    print "tesselated"
                    return False
            if x == self.start_corners[player-1][0] and y == self.start_corners[player-1][1]:
                corner = True
            for i,j in [[-1,-1],[-1,1],[1,-1],[1,1]]:
                if (x+i < 0 or x+i >= len(self.board) or y+j < 0 or y+j >= len(self.board[0])):
                    pass
                elif (self.board[x+i][y+j] == player):
                    corner = True  
        if (not corner):
            print "No connections"
            return False
        for tile in p:
            self.board[tile[0]][tile[1]] = player
        return True
        

def translatePiece(piece, rotations, flipped, location):
    p = rotPiece(piece, rotations)
    if (flipped):
        p = flipPiece(p)
    print p
    p = [[x+location[0],y+location[1]] for x,y in p]
    return p

def rotPiece(piece, rotations):
    print "rotations: %d" % (rotations)
    p = copy.deepcopy(piece)
    for i in range(rotations):
        max_y = max(i[1] for i in p)
        for j in range(len(p)):
            jx = p[j][0]
            jy = p[j][1]
            p[j][0], p[j][1] = max_y-jy, jx
    return p

def flipPiece(piece):
    p = copy.deepcopy(piece)
    max_y = max(i[1] for i in p)
    for j in range(len(p)):
        p[j][1] = max_y-p[j][1]
    return p

def printPiece(piece):
    fig = [['.' for i in range(5)] for j in range(5)]
    for x,y in piece:
        fig[y][x] = 'x'
    for i in range(len(fig)):
        for j in range(len(fig[i])):
            print fig[i][j],
        print '\n',

def test(game):
#    game = Game()
    curr_player = 1
    while True:
        print "Player %s" % (curr_player)
        for i in range(20):
            for j in range(20):
                if game.board [j][i]:
                    print game.board[j][i],
                else:
                    print '.',
            print ''
        key = input("Piece? ")
        rot = input("Rotation? ")
        flip = input("Flipped? ")
        ix = input("X? ")
        iy = input("Y? ")
        if game.play(curr_player, pieces[key], rot, flip, [ix,iy]):
            curr_player += 1
            if(curr_player > 4):
                curr_player = 1 
        else:
            print 'Invalid move!'
        
#    game.play(1, pieces['5W'], 1, 0, [0,0])
#    game.play(2, pieces['5V'], 1, 0, [17,0])
#    game.play(3, pieces['5V'], 2, 0, [17,17])
#    game.play(4, pieces['5V'], 3, 0, [0,17])
#    game.play(1, pieces['5I'], 0, 0, [3,3])
#    for row in game.board:
#        print row

    
#test()