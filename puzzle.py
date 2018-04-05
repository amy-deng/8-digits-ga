# coding: utf-8

import numpy as np
import copy


class EightDigits:
    def __init__(self):
        while True:
            self._puzzle = np.random.permutation(9).reshape((3, 3))
            self._this_puzzle = copy.copy(self._puzzle)
            self._blank = np.argwhere(0 == self._puzzle).flatten()
            self._this_blank = copy.copy(self._blank)
            if self.check_solution(np.delete(self._puzzle, self._blank[0] * 3 + self._blank[1], None)):  # 传入的是[]
                return

    @staticmethod
    def check_solution(puzzle):
        '''
        当初始状态棋局的棋子数列的逆序数是偶数时，八数码问题有解
        :param puzzle: [1,2,...]
        :return: 
        '''
        reverse = 0
        for idx, val in enumerate(puzzle):
            for prev in puzzle[:idx]:
                if prev > val:  # 前面的数比他小的个数
                    reverse += 1
        return not (reverse & 1)

    def move(self, step=None):
        '''
        移动操作
        :param step:
        :return:
        '''
        puzzle = self._puzzle
        zero = self._blank  # 0的位置，[0,1]
        step = np.array(step)  # 方向操作[-1,0]
        cell = zero + step  # cell 要移动的格子
        if cell[0] not in [0, 1, 2] or cell[1] not in [0, 1, 2]:  # 判断要移动的格子是否在九宫格内
            return
        puzzle[zero[0], zero[1]] = puzzle[cell[0], cell[1]]  # 要移动的数字放到原来0的位置
        puzzle[cell[0], cell[1]] = '0'  # 0放到要移动的数字原来的地方
        self._blank = cell
        self._puzzle = puzzle

    def distance(self):
        dis = 0
        for row in range(3):
            for col in range(3):
                v = (self._puzzle[row, col] + 8) % 9  # 应该的位置0-7
                dis += (row - int(v / 3)) ** 2 + (col - v % 3) ** 2  # 实际坐标和应该坐标 v/3 横坐标，v%3纵坐标
        return dis

    def reset_puzzle(self):
        self._puzzle = copy.copy(self._this_puzzle)
        self._blank = copy.copy(self._this_blank)
        return self

    def success(self):
        return self.distance() == 0

    # 返回对象的字符串表达式
    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in line]) \
                          for line in self._puzzle.tolist()])

    @property
    def puzzle(self):
        return self._puzzle
