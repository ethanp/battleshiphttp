import requests, random


battleship, carrier, destroyer, patrol, submarine = 'battleship', 'carrier', 'destroyer', 'patrol', 'submarine'

ship_lengths = {carrier: 5, battleship: 4, submarine: 3, destroyer: 3, patrol: 2}

unshot, miss, hit = range(3)
blank_stare, aggressive_mode = range(2)

boardWidth = 10
boardHeight = 10

class Battleship(object):
    def __init__(self):
        self.id = 'f0024225df1f' # TODO pass as param
        self.current_board = 'live_board_1' # TODO pass as param
        self.sunk_state = {
            battleship  : False,
            carrier     : False,
            destroyer   : False,
            patrol      : False,
            submarine   : False
        }
        self.last_shot_coords = (-1, -1)
        self.last_shot_hit = False

        # 0 for haven't shot, 1 for miss, 2 for hit
        self.game_board = [[unshot]*boardWidth for _ in range(boardHeight)]

        self.reset_board()

        # this is (in part) for continuing to maul a boat
        # once it has been hit once
        # TODO should be a Queue.Queue
        self.hit_list = []

        # use aggressive_mode for
        self.mode = blank_stare

    # TODO pass board as param
    # TODO refactor the URL to elsewhere
    def reset_board(self):
        url = 'https://student.people.co/api/challenge/battleship/%s/boards/%s' % (
            self.id, self.current_board)
        requests.delete(url)

    def shoot(self, coord):
        url = 'https://student.people.co/api/challenge/battleship/%s/boards/%s/%s' % (self.id, self.current_board, Battleship.toLocation(coord))
        r = requests.post(url).json()
        if self.has_been_shot(coord):
            print 'You shot at %s already' % coord
            return
        print 'Shooting at', coord
        if r['is_hit']:
            self.updateBoard(coord, hit)
            print 'You hit something'
        else:
            self.updateBoard(coord, miss)
            print 'You missed'

        return r['is_hit']

    # tested
    @staticmethod
    def toLocation(coord):
        row, col = coord
        assert 0 <= row < 10, 'invalid row'
        assert 0 <= col < 10, 'invalid col'
        col = 'ABCDEFGHIJ'[col]
        row += 1
        return '%s%d' % (col, row)

    def updateBoard(self, coords, val):
        row, col = coords
        self.game_board[row][col] = val


    def in_order_shot(self):
        # TODO should be be equal probability of shooting anywhere
        while True:
            empties = [(i, j) for i in range(boardWidth) for j in range(boardHeight) if not self.has_been_shot()]
            if not empties: return # game over
            randInd = random.randint(0, len(empties)-1)


        for i in range(boardWidth):
            for j in range(boardHeight):
                coord = i, j
                if not self.has_been_shot(coord):
                    if self.shoot(coord):
                        self.hit_list.append(coord)
                        if self.mode == aggressive_mode:
                            self.neighbor_shots() # was a hit

        # TODO collect unshot coordinates
        # TODO choose one at random to shoot at

    def has_been_shot(self, coord):
        i, j = coord
        return self.game_board[i][j] != unshot

    @staticmethod
    def find_neighbors(coord):
        i, j = coord
        up = i-1, j
        down = i+1, j
        left = i, j-1
        right = i, j+1
        return [up, down, left, right]

    @staticmethod
    def is_in_board(coord):
        i, j = coord
        return 0 <= i < boardWidth and 0 <= j < boardHeight

    # how about, when a hit is made, no matter what,
    # we shoot at all locations around that hit
    def neighbor_shots(self):
        while self.hit_list:
            next_up = self.hit_list.pop(0)
            directions = Battleship.find_neighbors(next_up)
            for coord in directions:
                if Battleship.is_in_board(coord):
                    if not self.has_been_shot(coord):
                        if self.shoot(coord): # was a hit too...
                            self.hit_list.append(coord)


    # TODO continue spree if there is one

    # TODO return to original strategy when the boat is sunk

a = Battleship()
a.in_order_shot()
