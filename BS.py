# -*- coding: utf-8 -*-
# @Time    : 13/4/2017 2:31 PM
# @Author  : Shen Tao
# @Site    : 
# @File    : BS.py
# @Software: PyCharm
from __future__ import division
from scipy.stats import norm
N = norm.cdf
n = norm.pdf
import numpy as np
def BSM(option_type, S, K, T, r, sigma, q=0.0):
    d1 = (np.log(S/ K) + ((r - q) + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'C':
        return S * np.exp(-q * T) * N(d1) - K * np.exp(-r * T) * N(d2)
    elif option_type=='P':
        return K * np.exp(-r * T) * N(-d2) - S * np.exp(-q * T) * N(-d1)
    else:
        print('option type is not included')
        return 0
def BS_vega(cp_flag,S,K,T,r,sigma,q=0.0):
    d1 = (np.log(S/K)+(r-q+sigma ** 2/2.0)*T)/(sigma*np.sqrt(T))
    return S * np.sqrt(T)*n(d1)
def implied_vol(option_price, option_type, S, K, T, r,q=0,precision = 1.0e-5,max_iteration = 100):
    sigma = 0.1
    for i in range(0, max_iteration):
        price = BSM(option_type, S, K, T, r, sigma,q)
        diff = option_price - price  # our root
        if (abs(diff) < precision):
            return sigma
        vega = BS_vega(option_type, S, K, T, r, sigma, q)
        sigma = sigma + diff/vega # f(x) / f'(x)
    # value wasn't found, return best guess so far
    return sigma
from time import time
t0=time()
for i in range(10000):
    BSM('C',10,10,1,0.05,0.1, q=0.0)
    implied_vol(1.0,'C',10,10,1,0.05)
print(time()-t0)
a = np.ones(10000)*10
b = np.ones(10000)
t0=time()
BSM('C',a,a,b,0.05,0.1, q=0.0)
for i in range(10000):
    implied_vol(1.0,'C',10,10,1,0.05)
print(time()-t0)