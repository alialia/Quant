# -*- coding: utf-8 -*-


# The following import is not necessary in Python 3 as true division is the default behavior.
# from __future__ import division

import numpy as np

def NS(beta0, beta1, beta2, lambda0, m):
    """
    Calculate the spot and forward rates using the Nelson-Siegel model.

    Parameters:
    beta0 (float): The level parameter.
    beta1 (float): The slope parameter.
    beta2 (float): The curvature parameter.
    lambda0 (float): The decay factor.
    m (float or array-like): The maturity or maturities. Cannot be zero or negative.

    Returns:
    list: A list containing the spot rate and the forward rate.

    Raises:
    ValueError: If 'm' is an empty array.
    ValueError: If any element in 'm' is less than the minimum threshold (1e-10).

    Notes:
    - The Nelson-Siegel model is used to fit the yield curve and is widely used in finance.
    - The function ensures numerical stability by checking for empty arrays and very small maturities.
    - The spot rate is calculated using the formula:
      \[
      \text{spot} = \beta_0 + (\beta_1 + \beta_2) \frac{1 - e^{-m / \lambda_0}}{m / \lambda_0} - \beta_2 e^{-m / \lambda_0}
      \]
    - The forward rate is calculated using the formula:
      \[
      \text{forward} = \beta_0 + \beta_1 e^{-m / \lambda_0} + \beta_2 \frac{m}{\lambda_0} e^{-m / \lambda_0}
      \]
    """
    # Define a small threshold to avoid numerical instability
    min_m = 1e-10

    # Check if m is an empty array
    if isinstance(m, (list, np.ndarray)) and len(m) == 0:
        raise ValueError("Maturity 'm' cannot be an empty array.")

    # Check if any element in m is less than the minimum threshold
    if np.any(m < min_m):
        raise ValueError(f"Maturity 'm' must be greater than or equal to {min_m}.")

    # Calculate k = m / lambda0
    k = m / lambda0

    # Calculate exp(-k) once to avoid redundant computation
    exp_neg_k = np.exp(-k)

    # Calculate the spot rate using the Nelson-Siegel formula
    spot = beta0 + (beta1 + beta2) * (1 - exp_neg_k) / k - beta2 * exp_neg_k

    # Calculate the forward rate using the Nelson-Siegel formula
    forward = beta0 + beta1 * exp_neg_k + beta2 * k * exp_neg_k

    return [spot, forward]
