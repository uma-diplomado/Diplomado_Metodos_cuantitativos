import multiprocessing as mp
import numpy as np
import math
import matplotlib.pyplot as plt
from time import time

def simulate_geometric_brownian_motion(p):
    M, I = p
      # time steps, paths
    S0 = 100; r = 0.05; sigma = 0.2; T = 1.0
      # model parameters
    dt = T / M
    paths = np.zeros((M + 1, I))
    paths[0] = S0
    for t in range(1, M + 1):
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                    sigma * math.sqrt(dt) * np.random.standard_normal(I))
    return paths

if __name__ == '__main__':
    I = 10000  # number of paths
    M = 50  # number of time steps
    t = 20  # number of tasks/simulations
    pool = mul.Pool(5)
    rel  = pool.map(f,[1,2,3,4,5,6,7,8,9,10])
    
    times = []
    for w in range(1, 5):
        t0 = time()
        pool = mp.Pool(processes=w)
          # the pool of workers
        result = pool.map(simulate_geometric_brownian_motion, t * [(M, I), ])
          # the mapping of the function to the list of parameter tuples
        times.append(time() - t0)

        print(rel)
        
    lt.plot(range(1, 5), times)
    plt.plot(range(1, 5), times, 'ro')
    plt.grid(True)
    plt.xlabel('number of processes')
    plt.ylabel('time in seconds')
    plt.title('%d Monte Carlo simulations' % t)   
        
        
        
        
        