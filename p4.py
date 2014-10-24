"""
p4.py
CS440 Assignment 4
Submitted by K. Brett Mulligan (eID: kbmulli)
This module uses constraint satisfaction to solve 
the problem of how many knights can be placed on a 
Chess board with no knights of the same color 
attacking each other. Run backtracking_solve, 
AC3_solve, or combined_solve with k knights on
size n chessboard.
"""

#################################################
# p4.py - Solve a CSP using various strategies
# by K. Brett Mulligan
# 16 Oct 2014
# CSU CS440
# Dr. Asa Ben-Hur
#################################################

import time
import re
import random
import math
import sys
import os
import copy

import search 
import csp

KNIGHT_CHAR1 = 'X'
KNIGHT_CHAR2 = 'O'
KNIGHT_CONFLICT = '#'

VERSBOSE_CONSTRAINTS = False


class Knights(csp.CSP):

    black_knights = []
    white_knights = []
    positions = []
    domains = {}
    neighbors = {}

    def __init__(self, k=8, n=4):
        self.boardlength = n

        self.vars = range(k*2)
        self.domains = {}

        for i in range(k):
            self.white_knights.append([-1,-1])
            self.black_knights.append([-1,-1])


        self.positions = self.generate_all_coords()

        for var in self.vars:
            self.domains[var] = list(self.positions)
            self.neighbors[var] = [x for x in self.vars if x != var]

        self.curr_domains = dict(self.domains)

        self.nassigns = 0

        # csp.CSP.__init__(self, self.vars, self.domains, self.neighbors, self.constraints)



    def __repr__(self):
        board = []
        for x in range(self.boardlength):
            board.append(['.' for x in range(self.boardlength)])

        for w in self.white_knights:
            if w in self.positions:
                if board[w[0]][w[1]] == '.':
                    board[w[0]][w[1]] = KNIGHT_CHAR1
                else:
                    board[w[0]][w[1]] = KNIGHT_CONFLICT

        for b in self.black_knights:
            if b in self.positions:
                if board[b[0]][b[1]] == '.':
                    board[b[0]][b[1]] = KNIGHT_CHAR2
                else:
                    board[b[0]][b[1]] = KNIGHT_CONFLICT

        for x in range(len(board)):
            board[x] = ' '.join(board[x])

        return '\n'.join(board)

    def display(self, a=None):
        if a:
            print self, '\nAssignment:\n', a
            total = 0
            for x in self.vars:
                add = self.nconflicts(x, a[x], a)
                total += add
                # print x, 'conflicts:', add
            print 'Total conflicts:', total
            print 'Conflicted:', self.conflicted_vars(a)
        else:
            print self, '\nAssignment:\nN/A'

    def print_curr_domains(self):
        for v in self.vars:
            print v, self.curr_domains[v]

    def update_knights_with_list(self, vals):
        self.white_knights = []
        self.black_knights = []

        if type(vals) is list:
            for x in range(len(vals)):
                if self.get_color(x) == 'white':
                    self.white_knights.append(vals[x])
                else:
                    self.black_knights.append(vals[x])
        else:
            print 'update_knights w/ list: invalid vals:', vals

    def update_knights_with_assignment(self, vals):
        self.white_knights = []
        self.black_knights = []

        if type(vals) is dict:
            for x in vals.keys():
                if self.get_color(x) == 'white':
                    self.white_knights.append(vals[x])
                else:
                    self.black_knights.append(vals[x])
        else:
            print 'update_knights w/ assignment: invalid vals:', vals

    # should return True if meeting all constraints
    def constraints(self, A, a, B, b):
        conflicted = False

        if VERSBOSE_CONSTRAINTS: print 'Comparing', A, a, 'and', B, b

        if (A == B):
            conflicted = False
            if VERSBOSE_CONSTRAINTS: print 'constraints: comparing knight to itself'
        elif (A != B) and (a == b):
            conflicted = True
            if VERSBOSE_CONSTRAINTS: print 'constraints: same point'
        elif self.same_color(A,B) and self.is_attacking(a,b):
            conflicted = True
            if VERSBOSE_CONSTRAINTS: print 'constraints: ARE attacking each other causing a conflict!'
        else:
            conflicted = False
            if VERSBOSE_CONSTRAINTS: print 'constraints: other case'

        if VERSBOSE_CONSTRAINTS: print 'Conflicted:', conflicted

        return not conflicted

    # should return True if meeting all constraints
    def constraints_backup(self, A, a, B, b):
        conflicted = False

        if VERSBOSE_CONSTRAINTS: print 'Comparing', A, a, 'and', B, b

        if (A == B):
            conflicted = False
            if VERSBOSE_CONSTRAINTS: print 'constraints: comparing knight to itself'
        elif (A != B) and (a == b):
            conflicted = True
            if VERSBOSE_CONSTRAINTS: print 'constraints: same point'
        elif not self.same_color(A,B):
            conflicted = False
            if VERSBOSE_CONSTRAINTS: print 'constraints: not same color, no need to check attacking'
        elif not self.is_attacking(a,b):
            conflicted = False
            if VERSBOSE_CONSTRAINTS: print 'constraints: not attacking each other'
        elif self.is_attacking(a,b):
            conflicted = True
            if VERSBOSE_CONSTRAINTS: print 'constraints: ARE attacking each other causing a conflict!'
        else:
            conflicted = True
            print 'constraints: unknown case'

        if VERSBOSE_CONSTRAINTS: print 'Conflicted:', conflicted

        return not conflicted

    def is_attacking(self, pos1, pos2):
        return (get_distance(pos1, pos2) == 3) and (pos1[0] != pos2[0]) and (pos1[1] != pos2[1])

    def same_color(self, A, B):
        return (self.get_color(A) == self.get_color(B))

    def get_color(self, knight):
        color = ''
        if (knight % 2 == 1):
            color = 'black'
        else:
            color = 'white'
        return color

    def generate_all_coords(self):
        coords = []
        for row in range(self.boardlength):
            for col in range(self.boardlength):
                coords.append((row, col))
        return coords

    def randomize(self):
        new_vals = {}
        for x in self.vars:
            new_vals[x] = random.choice(self.domains[x])
        return new_vals


# returns Manhattan distance from pos1 to pos2
def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def extract_solution(s):
    white = [s[x] for x in s.keys() if x % 2 == 0]
    black = [s[x] for x in s.keys() if x % 2 == 1]
    return white + black

def AC3_solve(k, n):
    knights = Knights(k, n)

    print 'AC3...'
    csp.AC3(knights)

    return

def backtracking_solve(k, n):
    knights = Knights(k, n)

    print 'Knights:'
    knights.display()


    print 'backtracking_search...'
    solution = csp.backtracking_search(knights, mcv=False, lcv=False, fc=False, mac=False)


    print ''
    if solution: knights.update_knights_with_assignment(solution)
    knights.display(solution)


    if solution:
        # print 'Solution:', solution
        sol = solution
    else:
        print 'No solution found.'
        sol = None

    return sol

def combined_solve(k, n):
    knights = Knights(k, n)
    csp.AC3(knights)
    solution = csp.backtracking_search(knights)
    return solution



def do_testing():

    NUM_KNIGHTS = 12  
    BOARD_LENGTH = 5
    
    bs = backtracking_solve(NUM_KNIGHTS, BOARD_LENGTH)
    
    




if __name__ == '__main__':
    do_testing()
