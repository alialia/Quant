a=0.2;
b=0.05;
sigma=0.1;
dt=0.001;
r0=0.04;
M=1000000;
r = r0*ones(M,1);
N=250;
T=N*dt;
c = 2*a/(1-exp(-a*T))/sigma^2;
for i=1:N
    r = r+a*(b-r)*dt+sigma*sqrt(r*dt).*normrnd(0,1,[M,1]).*(2*(r+a*(b-r)*dt+sigma*sqrt(r*dt).*normrnd(0,1,[M,1])>0)-1);
end
y=2*c*r;
% for detail of y, see https://en.wikipedia.org/wiki/Cox%E2%80%93Ingersoll%E2%80%93Ross_model
mean_theoretical = 2*c*(r0*exp(-a*N*dt)+b*(1-exp(-a*N*dt)));
var_theoretical = 4*c^2*(r0*sigma^2/a*(exp(-a*N*dt)-exp(-2*a*N*dt))+b*sigma^2/2/a*(1-exp(-a*N*dt))^2);
lambda=(var_theoretical-2*mean_theoretical)/2;
k = mean_theoretical-lambda;
excess_kurtosis_theoretical = 12*(k+4*lambda)/(k+2*lambda)^2;
skewness_theoretical = 2^1.5*(k+3*lambda)/(k+2*lambda)^1.5;
mean_sample = mean(y);
var_sample = var(y);
skewness_sample = skewness(y);
excess_kurtosis_sample = kurtosis(y)-3;
/*
The provided code snippet simulates the Cox-Ingersoll-Ross (CIR) model, which is used to describe the evolution of interest rates. The CIR model is a type of stochastic differential equation that ensures interest rates remain positive.

First, the parameters of the model are defined:

a (0.2) is the speed of mean reversion.
b (0.05) is the long-term mean level.
sigma (0.1) is the volatility.
dt (0.001) is the time step size.
r0 (0.04) is the initial interest rate.
M (1,000,000) is the number of simulations.
The initial interest rate vector r is created with all elements set to r0. The number of time steps N is set to 250, and the total time T is calculated as N * dt.

The constant c is calculated using the formula: [ c = \frac{2a}{(1 - \exp(-aT)) \sigma^2} ] This constant is used later in the transformation of the interest rate process.

The main loop runs for N iterations, updating the interest rate r at each time step using the CIR model's discretized form: [ r = r + a(b - r)dt + \sigma \sqrt{r dt} \cdot \text{normrnd}(0, 1, [M, 1]) \cdot (2 \cdot (r + a(b - r)dt + \sigma \sqrt{r dt} \cdot \text{normrnd}(0, 1, [M, 1]) > 0) - 1) ] This update ensures that the interest rates remain positive by adjusting the sign of the random term.

After the loop, the transformed variable y is calculated as: [ y = 2c \cdot r ] This transformation is related to the CIR model's properties and is used for further statistical analysis.

The theoretical mean and variance of y are calculated using the formulas: [ \text{mean_theoretical} = 2c \left( r0 \exp(-aNdt) + b(1 - \exp(-aNdt)) \right) ] [ \text{var_theoretical} = 4c^2 \left( \frac{r0 \sigma^2}{a} (\exp(-aNdt) - \exp(-2aNdt)) + \frac{b \sigma^2}{2a} (1 - \exp(-aNdt))^2 \right) ]

The parameters lambda and k are derived from the theoretical mean and variance: [ \lambda = \frac{\text{var_theoretical} - 2 \cdot \text{mean_theoretical}}{2} ] [ k = \text{mean_theoretical} - \lambda ]

The theoretical excess kurtosis and skewness are calculated as: [ \text{excess_kurtosis_theoretical} = \frac{12(k + 4\lambda)}{(k + 2\lambda)^2} ] [ \text{skewness_theoretical} = \frac{2^{1.5}(k + 3\lambda)}{(k + 2\lambda)^{1.5}} ]

Finally, the sample mean, variance, skewness, and excess kurtosis of y are calculated using the corresponding MATLAB functions: [ \text{mean_sample} = \text{mean}(y) ] [ \text{var_sample} = \text{var}(y) ] [ \text{skewness_sample} = \text{skewness}(y) ] [ \text{excess_kurtosis_sample} = \text{kurtosis}(y) - 3 ]

These sample statistics are compared to the theoretical values to validate the simulation.
