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
    
    times = []
    process_ = range(1,10)
    for w in process_:
        t0 = time()
        pool = mp.Pool(processes=w)
          # the pool of workers
        result = pool.map(simulate_geometric_brownian_motion, t * [(M, I), ])
          # the mapping of the function to the list of parameter tuples
        t_=time()-t0
        times.append(t_)
        print(t_)
        
        
    plt.plot(process_, times)
    plt.plot(process_, times, 'ro')
    plt.grid(True)
    plt.xlabel('number of processes')
    plt.ylabel('time in seconds')
    plt.title('%d Monte Carlo simulations' % t)
    plt.show()    
        
        
        
        
        