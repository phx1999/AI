import random
from Node import Node

def IC():
    Network = []
    Seeds = []
    NodeNum, EdgNum = 0, 0
    with open('NetHEPT.txt', 'r') as file:
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
                    Network.append(Node(0, 0))
                FirstLine = False
                continue
            outWeight = [int(S[1]), float(S[2])]
            Network[int(S[0])].add_outnei(outWeight)

    with open('seeds50.txt', 'r') as file:
        for line in file:
            num = int(line)
            Seeds.append(num)
            Network[num].active()

    Count = len(Seeds)
    while (len(Seeds)!=0):
        newSeeds = []
        for num in Seeds:
            for nei in Network[num].get_outnei():
                if Network[nei[0]].state == 0 and random.random() <= nei[1]:
                    Network[nei[0]].active()
                    newSeeds.append(nei[0])
        Count += len(newSeeds)
        Seeds = newSeeds
    return Count


if __name__ == "__main__":
    

    sun = 0.000
    for i in range(0, 100):
        sun += IC()
    print(sun / 100)
