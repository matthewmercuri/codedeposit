% Matthew Mercuri
% MTH 600 Final
% April 24, 2021


function V = Eur_Call_LVF_MC(S0, K, T, r, x, M, N)
    %
    % Price the European call option of the LVF model by the Monte Carlo method
    %
    % Input
    % S0 – initial stock price
    % K – strike price
    % T – maturity
    % r – risk free interest rate
    % x – vector parameters for the LVF σ, [x1, x2, x3]
    % M – number of simulated paths
    % N – number of time steps, i.e., δt = T /N.
    %
    % Output
    % V – European call option price at t = 0 and S0.
    
    % creating vector to store stock price at expiration
    S_finals = zeros(1, M);
    dt = T/N;  % constant value for delta t to use later
    
    % for loop to generate M simulations (paths)
    for i = 1:M
        S = zeros(1, N); % vector to store path's prices
        S(1, 1) = S0;  % assigning initial price as first value
        % for loop to generate stock price at each time step
        for j = 2:N
            % calculating volatitily by LVF model
            sigma = max([0.0, x(1)+(x(2)*S(j-1))+(x(3)*(S(j-1)^2))]);
            % calculating time step's price by LVF
            S(1, j) = S(1, j-1) + (r*S(1, j-1)*dt) + (sigma*S(1, j-1)*(normrnd(0, 1)*sqrt(dt))); 
        end
        S_finals(1, i) = S(1, N);  % storing result of final price
    end
    % finding value for call (each path)
    V_finals = S_finals - K;
    V_finals = max(V_finals, 0);
    
    % finding average value
    V_avg = mean(V_finals);
    
    % discounting for final price
    V = exp(-r*T)*V_avg;
end