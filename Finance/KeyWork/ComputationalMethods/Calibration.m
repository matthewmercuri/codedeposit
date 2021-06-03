% Matthew Mercuri
% MTH 600 Final
% April 24, 2021

% observed values
Ks = [0.80 0.85 0.90 0.95 1.00 1.05 1.10];
V_observed = [0.3570 0.2792 0.2146 0.1747 0.1425 0.1206 0.0676];

% initial values of x to start calibration
x01 = [0.2; 0.0; 0.0];
x02 = [0.2; 0.1; 0.01];

% configuring LM method to find the best values for x
options = optimoptions('lsqnonlin', 'SpecifyObjectiveGradient', true);
options.Algorithm = 'levenberg-marquardt';
options.Display = 'iter';

% using non-linear least squares and the above built-in function to
% achieve the best values for x
[x1, res1] = lsqnonlin(@myfun, x01, [], [], options);  % for x01
[x2, res2] = lsqnonlin(@myfun, x02, [], [], options);  % for x02

% displaying results in console
disp(x1)
disp(x2)

% using the optimal x values that were computed above to price our options
% creating vectors to store calibrated values
V_x1 = zeros(1, length(Ks));
V_x2 = zeros(1, length(Ks));

for b = 1:length(Ks)
    V_x1(1, b) = Eur_Call_LVF_MC(1, Ks(b), 0.25, 0.03, x1, 10000, 100);
    V_x2(1, b) = Eur_Call_LVF_MC(1, Ks(b), 0.25, 0.03, x2, 10000, 100);
end

% Plotting results
figure(1)
plot(Ks, V_x1, 'LineWidth', 1);
hold on;

plot(Ks, V_x2, 'LineWidth', 1);
plot(Ks, V_observed,'LineWidth', 1);
hold off;

title('Calibrating x with MC Method for Pricing Options (LVF Model)');
xlabel('Strike Price (K)');
ylabel('Initial Value V(K,0)');
axis('tight');
legend('MC 1', 'MC 2', 'Market');

% computing implied volatilities
i_mkt = blsimpv(1, Ks, 0.03, 0.25, V_observed);
i_mc1 = blsimpv(1, Ks, 0.03, 0.25, V_x1);
i_mc2 = blsimpv(1, Ks, 0.03, 0.25, V_x2);


% Plotting implied volatility
figure(2)
plot(Ks, i_mkt, 'ko')
hold on

plot(Ks, i_mc1, 'LineWidth', 1.5)
plot(Ks, i_mc2, 'LineWidth', 1.5)

axis('tight')
legend('Observed', 'Fit 1', 'Fit 2')
title('Implied Volatility')
xlabel('Strike Price (K)')
ylabel('Sigma')
hold off
