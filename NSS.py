# -*- coding: utf-8 -*-

import numpy as np

def SV(beta0, beta1, beta2, beta3, tau1, tau2, m):
    '''
    Calculate the spot rate and forward rate for given maturities using the Svensson model.

    :param beta0: Coefficient for the long-term level of the yield curve.
    :param beta1: Coefficient for the short-term component of the yield curve.
    :param beta2: Coefficient for the medium-term component of the yield curve.
    :param beta3: Coefficient for the second medium-term component of the yield curve.
    :param tau1: Decay factor for the first exponential term.
    :param tau2: Decay factor for the second exponential term.
    :param m: Maturities. Array or number, can't be zero.
    :return: Tuple containing the spot rate and forward rate corresponding to maturities m.
    '''
    k1 = m / tau1  # Calculate k1 as the ratio of maturity to tau1
    k2 = m / tau2  # Calculate k2 as the ratio of maturity to tau2
    exp1 = np.exp(-k1)  # Calculate the exponential decay for k1
    exp2 = np.exp(-k2)  # Calculate the exponential decay for k2
    # Calculate the spot rate using the Svensson model formula
    spot = beta0 + (beta1 + beta2) * (1 - exp1) / k1 - beta2 * exp1 + beta3 * ((1 - exp2) / k2 - exp2)
    # Calculate the forward rate using the Svensson model formula
    forward = beta0 + beta1 * exp1 + beta2 * k1 * exp1 + beta3 * k2 * exp2
    return [spot, forward]  # Return the spot rate and forward rate as a list