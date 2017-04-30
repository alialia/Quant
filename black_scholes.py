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
class BS(object):
    def __init__(self,option_type, S, K, T, r, sigma, q):

        vars = locals() # dict of local names
        self.__dict__.update(vars) # __dict__ holds and object's attributes
        del self.__dict__["self"] # don't need `self`
        self.T_sqrt = np.sqrt(T)
        self.d1 = (np.log(self.S / self.K) + ((r - q) + sigma ** 2 / 2) * T) / (self.sigma * self.T_sqrt)
        self.d2 = self.d1 - sigma * np.sqrt(T)
    def BSM(self):

        if self.option_type == 'C':
            return self.S * np.exp(-self.q * self.T) * N(self.d1) - self.K * np.exp(-self.r * self.T) * N(self.d2)
        elif self.option_type=='P':
            return self.K * np.exp(-self.r * self.T) * N(-self.d2) - self.S * np.exp(-self.q * self.T) * N(-self.d1)
        else:
            print 'option type is not included'
            return 0
    def Vega(self):
        return self.S * self.T_sqrt*n(self.d1)

    def Delta(self):
        if self.option_type == 'C':
            return N(self.d1)
        elif self.option_type == 'P':
            return -N(-self.d1)
        else:
            print 'option type is not included'
            return 0
    def Gamma(self):
        if self.option_type == 'C' or self.option_type == 'P':
            return n(self.d1)/(self.S*self.sigma*self.T_sqrt)
        else:
            print 'option type is not included'
            return 0

    def Theta(self):
        if self.option_type == 'C':
            return -(self.S * self.sigma*  n(self.d1))/  (2 * self.T_sqrt) - self.r * self.K * np.exp(-self.r * self.T) * N( self.d2)
        elif self.option_type == 'P':
            return -(self.S * self.sigma * n(self.d1)) / (2 * self.T_sqrt) + self.r * self.K * np.exp(-self.r * self.T) * N(-self.d2)
        else:
            print 'option type is not included'
            return 0
    def Rho(self):
        if self.option_type == 'C':
            return self.K*self.T*np.exp(-self.r*self.T)*N(self.d2)
        elif self.option_type == 'P':
            return -self.K * self.T * np.exp(-self.r * self.T) * N(-self.d2)
        else:
            print 'option type is not included'
            return 0
class  Implied_vol(object):
    def __init__(self,option_type, S, K, T, r, q):
        vars = locals() # dict of local names
        self.__dict__.update(vars) # __dict__ holds and object's attributes
        del self.__dict__["self"] # don't need `self`
        self.T_sqrt = np.sqrt(T)
    def implied_vol(self,option_price,precision = 1.0e-5,max_iteration = 100):
        self.sigma = 0.1
        for i in xrange(max_iteration):
            self.d1 =  (np.log(self.S / self.K) + ((self.r - self.q) + self.sigma ** 2 / 2) * self.T) / (self.sigma * self.T_sqrt)
            self.d2 = self.d1 - self.sigma * self.T_sqrt
            price = self.BSM()
            diff = option_price - price  # our root
            if (abs(diff) < precision):
                # print i
                return self.sigma
            vega = self.Vega()
            self.sigma = self.sigma + diff/vega # f(x) / f'(x)
        # value wasn't found, return best guess so far
        print 'max_iteration exceeds, defaut max_iteration is 100'
        return self.sigma
    def BSM(self):

        if self.option_type == 'C':
            return self.S * np.exp(-self.q * self.T) * N(self.d1) - self.K * np.exp(-self.r * self.T) * N(self.d2)
        elif self.option_type=='P':
            return self.K * np.exp(-self.r * self.T) * N(-self.d2) - self.S * np.exp(-self.q * self.T) * N(-self.d1)
        else:
            print 'option type is not included'
            return 0
    def Vega(self):
        return self.S * self.T_sqrt * n(self.d1)
from time import time
t0=time()
for i in xrange(1000):
    bs = BS('C',50,65,1,0.03,0.15, 0.02)
    bs.Delta()
    bs.Gamma()
    bs.Vega()
    bs.Rho()
    bs.Theta()
    bs.BSM()
    del bs
    a = Implied_vol('C',50,65,1,0.03,0.02)
    a.implied_vol(0.158842128257)
# print bs.BSM()
print time()-t0
a = Implied_vol('C',50,65,1,0.03,0.02)
print a.implied_vol(0.158842128257)
# a = np.ones(10000)*10
# b = np.ones(10000)
# t1=time()
# BSM('C',a,a,b,0.05,0.1, 0.0)
# for i in xrange(10000):
#     implied_vol(1.0,'C',10,10,1,0.05)
# print time()-t1
