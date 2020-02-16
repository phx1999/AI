import random
import os
from multiprocessing import Pool
from algorithm_ncs import ncs_c as ncs


def test(r: float, lam: float, epoch: int, N:int):
    print("process id is", os.getpid())
    # lam = 0.85 + 0.3 * random.random()
    # r = 0.9881
    # epoch = 24
    # N = 3


    print("lam", lam, "r", r, "epoch", epoch, "N", N)
    ncs_para = ncs.NCS_CParameter(tmax=300000, lambda_exp=lam, r=r, epoch=epoch, N=N)
    ncs_c = ncs.NCS_C(ncs_para, 12)
    ncs_res = ncs_c.loop(quiet=True, seeds=0)
    os.system(
        "echo " + str(r) +
        "," + str(lam) +
        "," + str(epoch) +
        "," + str(N) +
        "," + str(ncs_res) +
        " >> test12.csv")


if __name__ == '__main__':
    # float
    r_Min = 0.9916
    r_Max = 0.9917
    # float
    lam_Min = 1.006
    lam_Max = 1.01
    # int
    epoch_Min = 9
    epoch_Max = 9
    # int
    N_Min = 2
    N_Max = 2

    l = []

    os.system("echo r, lambda, epoch, N, ncs_res >> test12.csv")

    for i in range(5000):
        tup = (
            round(r_Min + (r_Max - r_Min) * random.random(), 9),
            round(lam_Min + (lam_Max - lam_Min) * random.random(), 9),
            random.randint(epoch_Min,epoch_Max),
            random.randint(N_Min, N_Max)
        )
        l.append(tup)


    print(l)
    pool = Pool(7)
    res = pool.starmap(test, l)
    pool.close()
    pool.join()
