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

    black_knights = []
    white_knights = []
    positions = []
    domains = {}
    neighbors = {}

    def __init__(self, k, n):
        self.boardlength = n

        self.vars = range(k*2)
        self.domains = {}

        for i in range(k):
            self.white_knights.append([0,0])
            self.black_knights.append([0,0])

        for var in self.vars:
            self.domains[var] = list(self.generate_all_coords())
            self.neighbors[var] = list(self.vars)

        self.curr_domains = dict(self.domains)

        self.nassigns = 0



    def __repr__(self):
        board = []
        for x in range(self.boardlength):
            board.append(['.' for x in range(self.boardlength)])

        for w in self.white_knights:
            board[w[0]][w[1]] = KNIGHT_CHAR1

        for b in self.black_knights:
            board[b[0]][b[1]] = KNIGHT_CHAR2

        for x in range(len(board)):
            board[x] = ' '.join(board[x])

        return '\n'.join(board)

    def update_knights(self, vals):
        self.white_knights = []
        self.black_knights = []

        for x in vals.keys():
            if x < len(vals.keys())/2:
                self.white_knights.append(vals[x])
            else:
                self.black_knights.append(vals[x])

    def constraints(self, A, a, B, b):
        not_conflicted = False

        if a == b:
            not_conflicted = False
            # print 'constraints: same point'
        elif not self.same_color(A,B):
            not_conflicted = True
            # print 'constraints: not same color, no need to check attacking'
        elif not self.is_attacking(a,b):
            not_conflicted = True
            # print 'constraints: not attacking each other'
        elif self.is_attacking(a,b):
            not_conflicted = False
            # print 'constraints: ARE attacking each other causing a conflict!'
        else:
            not_conflicted = False
            print 'constraints: unknown case'

        return not_conflicted

    def is_attacking(self, pos1, pos2):
        return (get_distance(pos1, pos2) == 3) and (pos1[0] != pos2[0]) and (pos1[1] != pos2[1])

    def same_color(self, A, B):
        return (self.get_color(A) == self.get_color(B))

    def get_color(self, knight):
        color = ''
        if (knight >= len(self.vars)/2):
            color = 'black'
        else:
            color = 'white'
        return color

    def generate_all_coords(self):
        for row in range(self.boardlength):
            for col in range(self.boardlength):
                self.positions.append((row, col))
        return self.positions

    def randomize(self):
        new_vals = {}
        for x in self.vars:
            new_vals[x] = random.choice(self.domains[x])
        return new_vals


# returns Manhattan distance from pos1 to pos2
def get_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def extract_solution(s):
    return [s[x] for x in s.keys()]

def AC3_solve(k, n):
    knights = Knights(k, n)

    solution = csp.AC3(knights)

    if solution:
        print 'Solution:', solution
    else:
        print 'No solution found.'

    return solution

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

    NUM_KNIGHTS = 14
    BOARD_LENGTH = 8

    knights = Knights(NUM_KNIGHTS, BOARD_LENGTH)
    print knights

    backtrack_sol = backtracking_solve(NUM_KNIGHTS, BOARD_LENGTH)
    knights.update_knights(backtrack_sol)
    print knights
    print ''


    knights = Knights(NUM_KNIGHTS, BOARD_LENGTH)
    print knights
    
    ac3_sol = AC3_solve(NUM_KNIGHTS, BOARD_LENGTH)
    knights.update_knights(ac3_sol)
    print knights
    print ''

    
    # knights.update_knights(knights.randomize())
    # print ''
    # print 'Randomize'
    # print knights
    # print ''


if __name__ == '__main__':
    do_testing()
