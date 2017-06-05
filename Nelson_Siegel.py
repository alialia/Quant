# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np
def NS(beta0, beta1, beta2, lambda0, m):
    # m: array or number, can't be zero!!!
    k = m / lambda0
    spot = beta0 + (beta1 + beta2) * (1 - np.exp(-k)) / k - beta2 * np.exp(-k)  # spot rate
    forward = beta0 + beta1 * np.exp(-k) + beta2 * k * np.exp(-k)  # forward rate
    return [spot, forward]
