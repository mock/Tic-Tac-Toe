#!/usr/bin/env python

##
##  Tic-Tac-Toe challenge for Cox Media Group
##
##  2012-03-12
##
##  mark mcintyre
##  mark@mocktech.net
##

from copy import copy

def debug(message, active=False):
    """
    simple function to print helpful statements if called
    """
    if active:
        print message


class Board(object):

    def __init__(self):
        """
        initialize the board
        """
        self.debug = False
        self.game_over = False
        self.players = ['O', 'X']
        self.wins = [[1, 2, 3], [4, 5, 6], [7, 8, 9],   ## horizontals
                     [1, 4, 7], [2, 5, 8], [3, 6, 9],   ## verticals
                     [1, 5, 9], [3, 5, 7]]              ## diagonals

        board = dict()
        for x in range(1, 10):
            board[x] = None
        self.board = board
        debug("board initialized", self.debug)

    def show_board(self, with_guide=False):
        """
        display the board with current values
        """
        guide = """ 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------\n 7 | 8 | 9 \n\n"""

        spot1 = self.board[1]
        if spot1 is None:
            spot1 = " "
        
        spot2 = self.board[2]
        if spot2 is None:
            spot2 = " "
        
        spot3 = self.board[3]
        if spot3 is None:
            spot3 = " "
        
        spot4 = self.board[4]
        if spot4 is None:
            spot4 = " "
        
        spot5 = self.board[5]
        if spot5 is None:
            spot5 = " "
        
        spot6 = self.board[6]
        if spot6 is None:
            spot6 = " "
        
        spot7 = self.board[7]
        if spot7 is None:
            spot7 = " "
        
        spot8 = self.board[8]
        if spot8 is None:
            spot8 = " "
        
        spot9 = self.board[9]
        if spot9 is None:
            spot9 = " "
 
        grid = """ %s | %s | %s \n-----------\n %s | %s | %s \n-----------\n %s | %s | %s \n""" % (spot1, spot2, spot3, spot4, spot5, spot6, spot7, spot8, spot9)
        
        if with_guide:
            print guide
        print grid
        return grid

    def _get_other_player(self, player):
        """
        get the other player
        """
        other_player = copy(self.players)
        other_player.pop(other_player.index(player))
        other_player = other_player[0]
        return other_player
    
    def check_row_for_block(self, row, opponent):
        """
        look for potential wins in this row for this opponent
        so that we can block it
        """
        count = 0
        open_spots = list()
        need_to_block = False

        debug("checking row %s to block opponent %s..." % (row, opponent), self.debug) 

        for i in row:
            if self.board[i] == opponent:
                count += 1
            elif self.board[i] is None:
                open_spots.append(i)

        if count == 2 and open_spots:
            debug("two in this row (need to block): %s" % row, self.debug)
            need_to_block = True

        return (open_spots, need_to_block)

    def check_row_for_win(self, row, this_player):
        """
        look for potential wins in this row for this player
        """
        count = 0
        open_spots = list()
        move_to_win = False

        debug("checking row %s for this player %s to win..." % (row, this_player), self.debug)

        for i in row:
            if self.board[i] == this_player:
                count += 1
            elif self.board[i] is None:
                open_spots.append(i)

        if count == 2 and open_spots:
            debug("two in this row (go for the win): %s" % row, self.debug)
            move_to_win = True

        return (open_spots, move_to_win)
 
    def find_best_spots(self, open_spots, this_player):
        """
        finding the best spot to play (when not blocking)
        
        strategy:
        
        1. winner
        2. block
           a. center
           b. corners
               exceptions: if two opposing corners
                   are not already in possession by the
                   opponent
                 or
                   already a block in opposite corner
         
        """

        ##
        ##  get all the spots which are occupied by the opponent 
        ##  and run them through the checks
        ##
        opponent = self._get_other_player(this_player)
        opponent_spots = [x for x in range(1, 10) if self.board[x] == opponent]

        ##
        ##  center check
        ##
        if self.board[5] is None:
            debug("the center is available, taking it", self.debug)
            return [5]

        ##
        ##  corners now
        ##
        corners = [1, 3, 7, 9]
        sides = [2, 4, 6, 8]

        ##
        ##  this exception needs to be handled differently first
        ##
        if (1 and 9 in opponent_spots) or (3 and 7 in opponent_spots):
            debug("opposing corners are occupied by opposition, take action!", self.debug)
            for spot in sides:
                if self.board[spot] is None:
                    return [spot]
        
        ##
        ##  if opposing corners are not a problem, get a corner
        ##
        debug("looking for a spot in the corner", self.debug)

        for spot in corners:
            if self.board[spot] is None:
                if (not ((spot in [1, 9] and (1 and 9 not in opponent_spots)) and (spot in [3, 7] and (3 and 7 not in opponent_spots)))) or (5 in opponent_spots):
                    return [spot]

        ##
        ##  if we didn't take a corner, take a side
        ##
        for spot in sides:
            if self.board[spot] is None:
                return [spot]
                
    def checking(self, opponent, spot):
        """
        given an opponent and spot on the board, it will return
        with either the spot to block or the spots available.
        """

        print "checking spots...\n"

        ##
        ##  get the other this player
        ##
        this_player = self._get_other_player(opponent)

        ##
        ##  go for the win first
        ##
        for row in self.wins:
            ##  check for winning moves
            spots, move_to_win = self.check_row_for_win(row, this_player)
            if move_to_win:
                debug("here's the spot for the win: %s" % spots, self.debug)
                return spots

        ##
        ##  look for blocks next
        ##
        open_spots = list()
        for row in self.wins:
            ##  is the spot just played by opponent in this row?
            if spot in row:
                spots, need_to_block = self.check_row_for_block(row, opponent)
                if need_to_block:
                    debug("need to block in this spot: %s" % spots, self.debug)
                    return spots
                else:
                    debug("adding available spots to the list: %s" % spots, self.debug)
                    open_spots.extend(spots)
            else:
                ##  get the list of all open spots to consider
                debug("spot not in this row, find empties in this row", self.debug)
                open_spots.extend([x for x in row if self.board[x] is None])

            debug("opens spots so far: %s" % open_spots, self.debug)

        ##
        ##  find the best spot from the list of open spots since
        ##  no winning spots were found
        ##
        best_spot = self.find_best_spots(open_spots, this_player)

        return best_spot
        
    def mark_the_board(self, player, spot):
        """
        place the player's mark and check for a win
        """
        try:
            if self.board[spot] is not None:
                return False
        except KeyError, ke:
            return False

        print "marking this spot %s with %s\n" % (spot, player)
        self.board[spot] = player
        self.game_over = self.check_for_winner()
        return True

    def process_turn(self, opponent, spot):
        """
        given a spot just played by opponent, determine the best move to make
        place a mark
        """
        ##
        ##  mark the board first with opponent's move
        ##
        if not self.mark_the_board(opponent, spot):
            print "space already filled, try another\n"
            return False

        if self.game_over:
            print "we have a winner!\n"
            return True

        ##
        ##  no winner yet, our turn
        ##
        try:
            ##  check the spot that was just marked
            our_spot = self.checking(opponent, spot)[0]

            this_player = self._get_other_player(opponent)
            if not self.mark_the_board(this_player, our_spot):
                print "something went wrong\n"
                return False

        except TypeError, te:
            ##  board is full, game over
            print "no more moves to make, no one wins\n"
            self.game_over = True
        
        return True
    
    def check_for_winner(self):
        """
        look the rows over for a winner
        """
        for row in self.wins:
            debug("checking this row for winner: %s" % row, self.debug)
            for char in self.players:
                debug("checking this player for winner: %s" % char, self.debug)
                player = char
                vals = map(lambda x: self.board[x], row)
                debug("vals = %s" % vals, self.debug)
                same = vals[0] == vals[1] == vals[2] == char
                debug("same = %s" % same, self.debug)
                if same:
                    return True
        return False



if __name__ == "__main__":

    ##
    ##  instaniate, yo
    ##
    board = Board()

    ##
    ##  get a player (opponent)
    ##
    opponent = ""
    while opponent not in board.players:
        opponent = raw_input("Choose X or O: ")
        opponent = opponent.upper()

    board.show_board(with_guide=True)

    ##
    ##  shall we play the game?
    ##
    while not board.game_over:
        spot = raw_input("Which spot? ")
        if spot:
            board.process_turn(opponent, int(spot))
            board.show_board()

    print "game over, man!  game over!\n"


