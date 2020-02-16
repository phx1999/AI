import random
import copy
from Node import Node

def TL():
    Network = []
    Seeds = []
    NodeNum, EdgNum = 0, 0
    # with open('network.txt', 'r') as file:
    with open('NetHept.txt', 'r') as file:
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
                    thresh = random.random()
                    if thresh <= 0.001:
                        Network.append(Node(1, thresh))
                    else:
                        Network.append(Node(0, thresh))
                FirstLine = False
                continue

            innerWeight = [int(S[0]), float(S[2])]
            Network[int(S[0])].add_outnei(int(S[1]))
            Network[int(S[1])].add_innei(innerWeight)

    # with open('seeds5.txt', 'r') as file:
    with open('seeds50.txt', 'r') as file:
        for line in file:
            num = int(line)
            if Network[num].state == 0:
                Seeds.append(num)
                Network[num].active()
    Count = len(Seeds)
    finish=False
    while (not finish):
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei].state==0:
                    total=0
                    for innei in Network[nei].get_innei():
                        if Network[innei[0]].state==1:
                            total+=innei[1]
                    if  total>=Network[nei].thresh:
                        Network[nei].active()
                        Seeds.append(nei)
        if  len(Seeds)>Count:
            Count=len(Seeds)
        else:
            finish =True
    return Count


if __name__ == "__main__":

    sun=0.000
    for i in range(0,100):
        sun+=TL()
    print(sun/100)