# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np

def SV(beta0, beta1, beta2, beta3, tau1, tau2, m):
    '''
    :param beta0:
    :param beta1:
    :param beta2:
    :param beta3:
    :param tau1:
    :param tau2:
    :param m: maturities. Array or number, can't be zero!!!
    :return: spot rate and forward rate corresponding to maturities m
    '''
    k1 = m / tau1
    k2 = m / tau2
    exp1 = np.exp(-k1)
    exp2 = np.exp(-k2)
    spot = beta0 + (beta1 + beta2) * (1 - exp1) / k1 - beta2 * exp1 + beta3 * ((1 - exp2) / k2 - exp2)  # spot rate
    forward = beta0 + beta1 * exp1 + beta2 * k1 * exp1 + beta3 * k2 * exp2  # forward rate
