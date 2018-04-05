# coding: utf-8

import numpy as np
from puzzle import EightDigits

OPERATOR = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class GeneticAlgorithm:
    def __init__(self, population_size=None, dna_size=None):
        self.p_size = population_size or 100
        self.d_size = dna_size or 100
        self.population = self.init_population(self.p_size, self.d_size)

    def init_population(self, p_size, d_size):
        return np.random.randint(0, 4, (p_size, d_size)).tolist()  # 0-3   population_size行，100列

    @staticmethod
    def cross(mum, dad, rate=0.75):
        '''
        交叉生成两个子代
        :param mum:
        :param dad:
        :param rate:
        :return:
        '''
        if mum == dad or np.random.ranf() > rate:
            return mum, dad
        sep = np.random.randint(0, len(mum))
        son = dad[:sep] + mum[sep:]
        daughter = mum[:sep] + dad[sep:]
        return daughter, son

    @staticmethod
    def mutate(child, rate=0.09):
        '''
        按一定概率变异
        :param child:
        :param rate:
        :return:
        '''
        for i in range(len(child)):
            if np.random.ranf() < rate:  # 返回浮点数 [0.0, 1.0)
                child[i] = np.random.randint(0, 4)
        return child

    def fit(self, evolve, member):
        '''
        根据dna进行移动
        :param evolve:
        :param member:
        :return: dna，适应度
        '''
        evolve = evolve.reset_puzzle()  #获得问题初始状态
        for dna in member:
            evolve.move(OPERATOR[dna])
            if evolve.success():
                break
        return member, 1.0 / (evolve.distance() + 1)  # distance可为0

    def update_fitness(self, evolve, population):
        for member in population:
            yield self.fit(evolve, member)

    @staticmethod
    def selection(p_with_f):
        '''
        转盘上面积较大的版块被选择的概率高
        :param p_with_f:
        :return:
        '''
        total_fitness = np.sum([fitness for (member, fitness) in p_with_f])
        fitness_block = np.random.ranf() * total_fitness
        fitness_sum = 0
        for (member, fitness) in p_with_f:
            fitness_sum += fitness
            if fitness_sum > fitness_block:  # 如果累计概率大于产生的随机数
                return member[:]  # 赋值

    def generate(self, evolve, population, individual=1):
        '''
        繁殖并生成指定数量的子代
        :param evolve: 进化的8字码
        :param population: 这一代的所有个体
        :param individual: 选择最优个体数
        :return: 所有子代集体，最优子代
        '''
        p_with_f = sorted(list(self.update_fitness(evolve, population)), reverse=True, key=lambda x:x[1])
        children = [member for (member, fitness) in p_with_f[:individual]]
        while len(children) < len(population):
            mum = self.selection(p_with_f)
            dad = self.selection(p_with_f)
            daughter, son = self.cross(mum, dad)  # 交叉
            children.extend([self.mutate(daughter), self.mutate(son)])  # 变异个体增加到子代集体中
        return children[:len(population)], p_with_f[0]

    def iteration(self):
        '''
        生成每一代的个体并进行淘汰筛选，直到正确
        :return:
        '''
        population = self.population
        puzzle = EightDigits()
        print('='*6,'puzzle','='*6)
        print(puzzle)
        print('='*20,'\n')
        i = 0
        while True:
            population, best = self.generate(puzzle, population)
            print(' -——————--', 'generation', i, '——————---')
            print('| Best fitness is ',best[1])
            self.fit(puzzle, best[0])
            print('| Grid now:',' '*21,'|')
            # print(puzzle)
            for row in range(3):
                print('|', puzzle._puzzle[row][0],'', puzzle.puzzle[row][1], '', puzzle._puzzle[row][2], ' ' * 23, '|')
            print('','-'*33,'' '\n')
            if best[1] == 1.0:
                print('Final DNA is ',best[0])
                break
            i += 1


if __name__ == "__main__":
    print('population_size = 100, dna_size = 50')
    p = GeneticAlgorithm(100, 80)
    p.iteration()
