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
