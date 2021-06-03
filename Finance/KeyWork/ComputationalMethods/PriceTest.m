% Matthew Mercuri
% MTH 600 Final
% April 24, 2021

% This file calls two functions to compute the value of the same European
% call option. The first uses a Monte Carlo method and the second use an
% explicit method (FD PDE solution). Please note the input parameters are
% slightly different depending on the method

% Monte Carlo Method
V_mc = Eur_Call_LVF_MC(1, 1, 0.25, 0.03, [0.2 0.001 0.003], 10000, 100);

% Explicit Method
V_e = Eur_Call_LVF_FD(1, 1, 0.25, 0.03, [0.2 0.001 0.003], 3, 30, 100);

fprintf('The value for the call using the MC method is: $%d \n', V_mc)
fprintf('The value for the call using the explicit method is: $%d \n', V_e)
