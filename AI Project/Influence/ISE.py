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


class Worker(mp.Process):
    def __init__(self, inQ, outQ, random_seed, file_name, seed, model, time_limit):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ
        self.file_name = file_name
        self.seed = seed
        self.model = model
        self.time_limit = time_limit
        np.random.seed(random_seed)  # 如果子进程的任务是有随机性的，一定要给每个子进程不同的随机数种子，否则就在重复相同的结果了

    def run(self):
        while True:
            if self.model == "IC":
                ans = IC(copy.deepcopy(self.file_name),copy.deepcopy(self.seed))  # 执行任务
            else:
                ans = TL(copy.deepcopy(self.file_name), copy.deepcopy(self.seed))
            self.outQ.put(ans)  # 返回结果


def create_worker(num, file_name, seed, model, time_limit):
    '''
    创建子进程备用
    :param num: 多线程数量
    '''
    for i in range(num):
        worker.append(Worker(mp.Queue(), mp.Queue(), np.random.randint(0, 10 ** 9), file_name, seed, model, time_limit))
        worker[i].start()


def finish_worker():
    '''
    关闭所有子线程
    '''
    for w in worker:
        w.terminate()


def TL(Network, Seeds):
    finish = False
    Count=len(Seeds)
    while len(Seeds)!=0:
        newSeeds=[]
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei[0]].state == 0:
                    total = 0
                    for innei in Network[nei[0]].get_innei():
                        if Network[innei[0]].state == 1:
                            total += innei[1]
                    if Network[nei[0]].thresh==-1:
                        Network[nei[0]].set_thresh(random.random())
                    if total >= Network[nei[0]].thresh:
                        Network[nei[0]].active()
                        newSeeds.append(nei[0])
        Count+=len(newSeeds)
        Seeds=newSeeds

    return Count


def IC(Network, Seeds):
    Count = len(Seeds)
    while (len(Seeds) != 0):
        newSeeds = []
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei[0]].state == 0 and random.random() <= nei[1]:
                    Network[nei[0]].active()
                    newSeeds.append(nei[0])
        Count += len(newSeeds)
        Seeds = newSeeds
    return Count


if __name__ == '__main__':
    # '''
    # 从命令行读参数示例
    # '''
    # print("从命令行读参数示例")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='NetHEPT.txt')
    parser.add_argument('-k', '--seed', type=str, default='seeds50.txt')
    parser.add_argument('-m', '--model', type=str, default='LT')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit
    start = time.time()
    # print(file_name, seed, model, time_limit)

    # file_name="network.txt"
    # seed="seeds5.txt"
    # model="TL"
    # time_limit=120
    # file_name="NetHEPT.txt"
    # seed="seeds50.txt"
    Network = []

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
    Seeds=[]
    with open(seed, 'r') as file:
        for line in file:
            num = int(line)
            if Network[num].state == 0:
                Seeds.append(num)
                Network[num].active()
    np.random.seed(0)
    worker = []
    worker_num = 8
    create_worker(worker_num, Network, Seeds, model, time_limit)
    Task = [np.random.randint(0, 10, 2) for i in range(100)]  # 生成16个随机任务， 每个任务是2个整数， 需要计算两数之和与积
    for i, t in enumerate(Task):
        worker[i % worker_num].inQ.put(t)  # 根据编号取模， 将任务平均分配到子进程上
    result = 0.0
    num = 0
    for i, t in enumerate(Task):
        num = i
        result += worker[i % worker_num].outQ.get()  # 用同样的规则取回结果， 如果任务尚未完成，此处会阻塞等待子进程完成任务
    print(result / (num + 1))
    finish_worker()
    #
    # '''
    # 程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
    # '''
    sys.stdout.flush()

#
# # -*- coding: utf-8 -*-
# # written by mark zeng 2018-11-14
# # modified by Yao Zhao 2019-10-30
#
# import multiprocessing as mp
# import time
# import sys
# import argparse
# import os
# import numpy as np
# import random
# from Node import Node
#
# class Worker(mp.Process):
#     def __init__ (self, inQ, outQ, random_seed,file_name,seed,model,time_limit):
#         super(Worker, self).__init__(target=self.start)
#         self.inQ = inQ
#         self.outQ = outQ
#         self.file_name=file_name
#         self.seed=seed
#         self.model=model
#         self.time_limit=time_limit
#         np.random.seed(random_seed)  #  如果子进程的任务是有随机性的，一定要给每个子进程不同的随机数种子，否则就在重复相同的结果了
#
#     def run (self):
#         while True:
#             if  self.model=="IC":
#                 ans=IC(self.file_name,self.seed)  # 执行任务
#             else:
#                 ans=TL(self.file_name,self.seed)
#             self.outQ.put(ans)  # 返回结果
#
#
# def create_worker (num,file_name,seed,model,time_limit):
#     '''
#     创建子进程备用
#     :param num: 多线程数量
#     '''
#     for i in range(num):
#         worker.append(Worker(mp.Queue(), mp.Queue(), np.random.randint(0, 10 ** 9),file_name,seed,model,time_limit))
#         worker[i].start()
#
#
# def finish_worker ():
#     '''
#     关闭所有子线程
#     '''
#     for w in worker:
#         w.terminate()
#
# def TL(file_name,seed):
#     Network = []
#     Seeds = []
#     NodeNum, EdgNum = 0, 0
#     # with open('network.txt', 'r') as file:
#     with open(file_name, 'r') as file:
#         FirstLine = True
#         for line in file:
#             S = line.split(" ")
#             if FirstLine:
#                 NodeNum = int(S[0])
#                 EdgNum = int(S[1])
#                 for i in range(0, NodeNum + 1):
#                     if i == 0:
#                         Network.append([])
#                         continue
#                     thresh = random.random()
#                     if thresh <= 0.001:
#                         Network.append(Node(1, thresh))
#                     else:
#                         Network.append(Node(0, thresh))
#                 FirstLine = False
#                 continue
#
#             innerWeight = [int(S[0]), float(S[2])]
#             Network[int(S[0])].add_outnei(int(S[1]))
#             Network[int(S[1])].add_innei(innerWeight)
#
#     # with open('seeds5.txt', 'r') as file:
#     with open(seed, 'r') as file:
#         for line in file:
#             num = int(line)
#             if Network[num].state == 0:
#                 Seeds.append(num)
#                 Network[num].active()
#     Count = len(Seeds)
#     finish=False
#     while (not finish):
#         for num in Seeds:
#             for nei in Network[num].get_outnei():
#                 if Network[nei].state==0:
#                     total=0
#                     for innei in Network[nei].get_innei():
#                         if Network[innei[0]].state==1:
#                             total+=innei[1]
#                     if  total>=Network[nei].thresh:
#                         Network[nei].active()
#                         Seeds.append(nei)
#         if  len(Seeds)>Count:
#             Count=len(Seeds)
#         else:
#             finish =True
#     return Count
#
# def IC(file_name,seed):
#     Network = []
#     Seeds = []
#     NodeNum, EdgNum = 0, 0
#     with open(file_name, 'r') as file:
#         FirstLine = True
#         for line in file:
#             S = line.split(" ")
#             if FirstLine:
#                 NodeNum = int(S[0])
#                 EdgNum = int(S[1])
#                 for i in range(0, NodeNum + 1):
#                     if i == 0:
#                         Network.append([])
#                         continue
#                     Network.append(Node(0, 0))
#                 FirstLine = False
#                 continue
#             outWeight = [int(S[1]), float(S[2])]
#             Network[int(S[0])].add_outnei(outWeight)
#
#     with open(seed, 'r') as file:
#         for line in file:
#             num = int(line)
#             Seeds.append(num)
#             Network[num].active()
#
#     Count = len(Seeds)
#     while (len(Seeds)!=0):
#         newSeeds = []
#         for num in Seeds:
#             for nei in Network[num].get_outnei():
#                 if Network[nei[0]].state == 0 and random.random() <= nei[1]:
#                     Network[nei[0]].active()
#                     newSeeds.append(nei[0])
#         Count += len(newSeeds)
#         Seeds = newSeeds
#     return Count
#
#
# if __name__ == '__main__':
#     # '''
#     # 从命令行读参数示例
#     # '''
#     # print("从命令行读参数示例")
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-i', '--file_name', type=str, default='network.txt')
#     parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
#     parser.add_argument('-m', '--model', type=str, default='IC')
#     parser.add_argument('-t', '--time_limit', type=int, default=60)
#
#     args = parser.parse_args()
#     file_name = args.file_name
#     seed = args.seed
#     model = args.model
#     time_limit = args.time_limit
#     start=time.time()
#     # print(file_name, seed, model, time_limit)
#
#
#     # file_name="network.txt"
#     # seed="seeds5.txt"
#     # model="TL"
#     # time_limit=120
#     # file_name="NetHEPT.txt"
#     # seed="seeds50.txt"
#
#     np.random.seed(0)
#     worker = []
#     worker_num = 8
#     create_worker(worker_num,file_name,seed,model,time_limit)
#     Task = [np.random.randint(0, 10, 2) for i in range(1000)]  # 生成16个随机任务， 每个任务是2个整数， 需要计算两数之和与积
#     for i, t in enumerate(Task):
#         worker[i % worker_num].inQ.put(t)  # 根据编号取模， 将任务平均分配到子进程上
#     result =0.0
#     num=0
#     for i, t in enumerate(Task):
#         num=i
#         result+=worker[i % worker_num].outQ.get() # 用同样的规则取回结果， 如果任务尚未完成，此处会阻塞等待子进程完成任务
#         if time.time()-start>=time_limit-1:
#             break
#     print(result/(num+1))
#     finish_worker()
#     #
#     # '''
#     # 程序结束后强制退出，跳过垃圾回收时间, 如果没有这个操作会额外需要几秒程序才能完全退出
#     # '''
#     sys.stdout.flush()