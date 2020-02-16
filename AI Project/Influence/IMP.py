# -*- coding: utf-8 -*-
# written by mark zeng 2018-11-14
# modified by Yao Zhao 2019-10-30

import multiprocessing as mp
import time
import sys
import argparse
import os
import numpy as np
import random
from Node import Node
import copy
import heapq


def TL(Network, Seeds):
    change = []
    Count = len(Seeds)
    while len(Seeds) != 0:
        newSeeds = []
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei[0]].state == 0:
                    total = 0
                    for innei in Network[nei[0]].get_innei():
                        if Network[innei[0]].state == 1:
                            total += innei[1]
                    if Network[nei[0]].thresh == -1:
                        Network[nei[0]].set_thresh(random.random())
                    if total >= Network[nei[0]].thresh:
                        Network[nei[0]].active()
                        change.append(nei[0])
                        newSeeds.append(nei[0])
        Count += len(newSeeds)
        Seeds = newSeeds
    for i in change:
        Network[i].unactive()
    return Count


def IC(Network, Seeds):
    change = []
    Count = len(Seeds)
    while (len(Seeds) != 0):
        newSeeds = []
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei[0]].state == 0 and random.random() <= nei[1]:
                    Network[nei[0]].active()
                    change.append(nei[0])
                    newSeeds.append(nei[0])
        Count += len(newSeeds)
        Seeds = newSeeds
    for i in change:
        Network[i].unactive()
    return Count


if __name__ == '__main__':
    # '''
    # 从命令行读参数示例
    # '''
    # print("从命令行读参数示例")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--seedCount', type=int, default=5)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seedCount = args.seedCount
    model = args.model
    time_limit = args.time_limit
    start = time.time()
    # print(file_name, seed, model, time_limit)

    # file_name="network.txt"
    # seed=5
    # model="TL"
    # time_limit=120
    # file_name="NetHEPT.txt"
    # seed="seeds50.txt"
    Network = []
    NodeNum = 0
    with open(file_name, 'r') as file:
        FirstLine = True
        for line in file:
            S = line.split(" ")
            if FirstLine:
                NodeNum = int(S[0])
                EdgNum = int(S[1])
                for i in range(0, NodeNum + 1):
                    if i == 0:
                        Network.append([])
                        continue
                    Network.append(Node(0, -1))
                FirstLine = False
                continue

            innerWeight = [int(S[0]), float(S[2])]
            outWeight = [int(S[1]), float(S[2])]
            Network[int(S[0])].add_outnei(outWeight)
            Network[int(S[1])].add_innei(innerWeight)
    target_seed = []
    dd = []
    label = []
    label.append(0)
    degree_rank = heapq
    if seedCount == 5:
        run_num = 400
        for i in range(1, NodeNum + 1):
            label.append(0)
            target_seed.append(i)
    else:

        run_num = 50
        for i in range(1, NodeNum + 1):
            degree_rank.heappush(dd, [-1 * len(Network[i].outnei), i])
            label.append(0)
        if seedCount * 10 < NodeNum:
            while len(target_seed) < seedCount * 10:
                target_seed.append(degree_rank.heappop(dd)[1])

    Seeds = []
    total = 0
    qq = heapq
    xx = []
    # print("start")
    for node in target_seed:
        # print(node)
        if Network[node].state == 0:
            Network[node].active()
            Seeds.append(node)
            # print("start",time.time())
            if model == "IC":
                result = IC(Network, copy.copy(Seeds))
            else:
                result = TL(Network, copy.copy(Seeds))
            # print("end",time.time())
            Seeds.pop()
            Network[node].unactive()
            qq.heappush(xx, (-1 * result, node))

    next = qq.heappop(xx)
    Seeds.append(next[1])
    Network[next[1]].active()
    total += -1 * next[0]
    print(next[1])
    # print(total)
    while len(Seeds) < seedCount:
        top = qq.heappop(xx)
        node = top[1]
        label[node] = len(Seeds)
        Network[node].active()
        Seeds.append(node)
        result = 0
        for i in range(run_num):
            if model == "IC":
                result += IC(Network, copy.copy(Seeds))
            else:
                result += TL(Network, copy.copy(Seeds))
        result = result / run_num
        # print(-1 * (result-total))
        Seeds.pop()
        Network[node].unactive()
        qq.heappush(xx, (-1 * (result - total), node))
        check = qq.heappop(xx)
        if label[check[1]] == len(Seeds):
            Seeds.append(check[1])
            Network[check[1]].active()
            total += -1 * check[0]
            print(check[1])
            print("put " +str(check[1]) + "  total " + str(total))
        else:
            qq.heappush(xx, check)
    # print("finish")
