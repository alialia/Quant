# -*- coding: utf-8 -*-
# @Time    : 13/4/2017 2:31 PM
# @Author  : Shen Tao
# @Site    : 
# @File    : BS.py
# @Software: PyCharm
from scipy.stats import norm
N = norm.cdf
n = norm.pdf
import numpy as np

    
def monte_carlo_option_pricing(S0, K, T, r, sigma, M, option_type='call', notional=1.0):
    """
    Monte Carlo simulation to price a European option (without intermediate dates).
    Also computes the standard error of the estimate.
    
    Parameters:
    S0 : float
        Initial stock price.
    K : float
        Strike price.
    T : float
        Time to expiration in years.
    r : float
        Risk-free interest rate.
    sigma : float
        Volatility of the stock (standard deviation of stock's returns).
    M : int
        Number of simulated price paths (Monte Carlo simulations).
    option_type : str, optional
        Type of option, either 'call', 'put', 'digital_call', or 'digital_put'. Default is 'call'.
    notional : float, optional
        Notional amount of the option. Default is 1.0.
    
    Returns:
    tuple(float, float)
        Estimated price of the European option and its standard error.
    """
    # Simulate the stock price at maturity using the GBM formula
    z = np.random.standard_normal(M)  # Generate random normal variables
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    
    # Calculate the payoff for each simulation at maturity
    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - ST, 0)
    elif option_type == 'digital_call':
        payoffs = np.where(ST > K, 1, 0)
    elif option_type == 'digital_put':
        payoffs = np.where(ST < K, 1, 0)
    else:
        raise ValueError("option_type must be one of 'call', 'put', 'digital_call', or 'digital_put'")
    
    # Apply the notional amount to the payoffs
    payoffs *= notional
    
    # Discount the payoff back to present value
    discounted_payoffs = np.exp(-r * T) * payoffs
    
    # Estimate the option price as the mean of the discounted payoffs
    option_price = np.mean(discounted_payoffs)
    
    # Calculate the standard error
    standard_error = np.std(discounted_payoffs) / np.sqrt(M)
    
    return option_price, standard_error

# Example usage:
S0 = 1.05    # Initial stock price
K =  1.35    # Strike price
T = 5       # Time to expiration in years
r = 0.02    # Risk-free interest rate
sigma = 0.08 # Volatility of the stock
M = 1000000   # Number of simulated price paths

call_price, std_error = monte_carlo_call_option_maturity(S0, K, T, r, sigma, M)
print(f"Estimated price of the European call option: {call_price:.4f}")
print(f"Standard error of the estimated call price: {std_error:.6f}")

def BSMAnalytical(option_type, S, K, T, r, sigma, q=0.0):
    """
    计算欧式期权的BSM理论价格，包括普通欧式期权和数字期权。
    
    参数:
    - option_type: 期权类型，'C' 表示普通看涨期权，'P' 表示普通看跌期权，
                   'DC' 表示数字看涨期权，'DP' 表示数字看跌期权。
    - S: 标的资产当前价格。
    - K: 期权行权价。
    - T: 期权到期时间（以年为单位）。
    - r: 无风险利率。
    - sigma: 标的资产的年化波动率。
    - q: 标的资产的收益率（如股息率，默认为0）。
    
    返回值:
    - 期权的理论价格。
    """
    # 计算d1和d2，这是BSM公式中的重要组成部分
    d1 = (np.log(S/ K) + ((r - q) + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 根据期权类型计算理论价格
    if option_type == 'C':
        # 普通看涨期权的理论价格计算公式
        return S * np.exp(-q * T) * N(d1) - K * np.exp(-r * T) * N(d2)
    elif option_type == 'P':
        # 普通看跌期权的理论价格计算公式
        return K * np.exp(-r * T) * N(-d2) - S * np.exp(-q * T) * N(-d1)
    elif option_type == 'DC':
        # 数字看涨期权的理论价格计算公式
        return np.exp(-r * T) * N(d2)
    elif option_type == 'DP':
        # 数字看跌期权的理论价格计算公式
        return np.exp(-r * T) * N(-d2)
    else:
        # 如果期权类型不正确，则输出错误信息并返回0
        print('option type is not included')
        return 0
def BS_vega(option_type, S, K, T, r, sigma, q=0.0):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2.0) * T) / (sigma * np.sqrt(T))
    if option_type in ['C', 'P']:
        return S * np.sqrt(T) * n(d1)
    elif option_type in ['DC', 'DP']:
        return np.exp(-r * T) * np.sqrt(T) * n(d1)
    else:
        raise ValueError("option_type must be one of 'C', 'P', 'DC', or 'DP'")
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
# from time import time
# t0=time()
# for i in range(10000):
#     BSM('C',10,10,1,0.05,0.1, q=0.0)
#     implied_vol(1.0,'C',10,10,1,0.05)
# print(time()-t0)
# a = np.ones(10000)*10
# b = np.ones(10000)
# t0=time()
# BSM('C',a,a,b,0.05,0.1, q=0.0)
# for i in range(10000):
#     implied_vol(1.0,'C',10,10,1,0.05)
# print(time()-t0)

analytical = BSMAnalytical('C',S0,K,T,r,sigma, q=0.0)
print(analytical)