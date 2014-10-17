"""
p4.py
CS440 Assignment 4
Submitted by K. Brett Mulligan (eID: kbmulli)
This module ...
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


class Knights(csp.CSP):

    knights = []
    positions = []
    domains = {}
    neighbors = {}

    def __init__(self, k, n):
        self.boardlength = n

        self.vars = range(k)
        self.domains = {}

        for i in range(k):
            self.knights.append([0,0])

        for var in self.vars:
            self.domains[var] = list(self.generate_all_coords())
            self.neighbors[var] = list(self.vars)

        self.curr_domains = dict(self.domains)

        self.nassigns = 0



    def __repr__(self):
        board = []
        for x in range(self.boardlength):
            board.append(['.' for x in range(self.boardlength)])

        for k in self.knights:
            board[k[0]][k[1]] = KNIGHT_CHAR1

        for x in range(len(board)):
            board[x] = ' '.join(board[x])

        return '\n'.join(board)

    def update_knights(self, vals):
        self.knights = []
        for x in vals.keys():
            self.knights.append(vals[x])

    def constraints(self, A, a, B, b):
        not_conflicted = False

        if not (get_distance(a, b) == 3 and a[0] != b[0] and a[1] != b[1]) and a != b:
            not_conflicted = True

        return not_conflicted

    def generate_all_coords(self):
        for row in range(self.boardlength):
            for col in range(self.boardlength):
                self.positions.append((row, col))
        return self.positions


# returns Manhattan distance from pos1 to pos2
def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_attacking(pos1, pos2):
    return True

def AC3_solve(k, n):
    notimplemented

def backtracking_solve(k, n):
    knights = Knights(k, n)

    solution = csp.backtracking_search(knights)

    if solution:
        print 'Solution:', solution
    else:
        print 'No solution found.'

    return solution

def combined_solve(k, n):
    notimplemented


def do_testing():
    knights = Knights(8, 8)
    print knights

    knights.update_knights(backtracking_solve(24, 8))
    print knights    



if __name__ == '__main__':
    do_testing()
