import matplotlib.pyplot as plt
import numpy as np
from time import time
import multiprocessing as mp
import numba

def bsm_mcs_valuation(strike):
    ''' Estimador de Calls europeos con BS.
    Parameters
    ==========
    strike : float
    precio strike de la opción
    Resultados
    =======
    value : float
    estimador del valor presente del call
    '''
    T = 1
    N = 365 * T
    sigma = 0.02
    r= 0.02
    t = np.linspace(T/N,T,N)
    nSims = 100000
    S0=100

    Sims = np.random.normal(0,1,(nSims,N))
    Asset=S0*np.exp((r-0.5*sigma**2)*t+sigma*np.sqrt(t)*Sims)
    price = np.mean(np.maximum(Asset[:,-1]-strike,0))*np.exp(-r*T)
    return(price)
    
if __name__ == '__main__':
    print('Sequential Valuation')
    strikes= np.linspace(80,120,100)
    t_=time()
    option_values_seq = [bsm_mcs_valuation(strike) for strike in strikes]
    print('Time in seconds:')
    print(time()-t_)
    
    print('Paralell Valuation with 10 processes')
    
    pool = mp.Pool(processes=10)
    t0 = time()
    option_values_par = pool.map(bsm_mcs_valuation, strikes)
    print('Time in seconds:')
    print(time()-t0)

    print('Numba processing')
    bsm_mcs_valuation_nb = numba.jit(bsm_mcs_valuation)
    t_=time()
    option_values_num = [bsm_mcs_valuation_nb(strike) for strike in strikes]
    print('Time in seconds:')
    print(time()-t_)
        
    plt.figure(figsize=(8, 4))
    plt.plot(strikes, option_values_seq, 'b',label = 'sequential')
    plt.plot(strikes, option_values_num, 'b*',label = 'numba')
    plt.plot(strikes, option_values_par, 'r.',label = 'paralell')
    plt.grid(True)
    plt.xlabel('strikes')
    plt.ylabel('European call option values')
    plt.legend()
    plt.show()   