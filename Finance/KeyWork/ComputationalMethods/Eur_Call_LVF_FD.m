% Matthew Mercuri
% MTH 600 Final
% April 24, 2021

function V0 = Eur_Call_LVF_FD(S0, K, T, r, x, Smax, M, N)
    %
    % Price the European call option of the LVF model by the explicit finite difference method.
    %
    % Input
    % S0 – initial stock price
    % K – strike price
    % T – maturity
    % r – risk free interest rate
    % x – vector parameters for the LVF σ, [x1, x2, x3]
    % Smax – upper bound of the stock price
    % M – number of stock price difference, i.e., δS = Smax/M
    % N – number of time steps, i.e., δt = T /N.
    %
    % Output
    % V 0 – European call option price at t = 0 and S0.
    
    % computing necessary constants
    dS = Smax/M;  % increments for stock price
    dtau = T/N; % incremens for time steps
    
    % creating vector of all possible stock prices
    S = 0:dS:Smax;
    
    % creating matrix to represent solutions to PDE (grid)
    V = zeros(N,M+1);
    
    % computing initial conditions for each price and saving the result to
    % our grid
    for i = 1:M+1
        V(1,i) = max((S(i) - K), 0);
    end
    
    for n = 1:N-1
        % computing boundary conditions for each price of 0 and Smax
        V(n+1, M+1) = V(n, M+1);  % this is just payoff of Smax
        V(n+1, 1) = V(n, 1)*((1-r)*dtau); % this is just 0
        
        % using finite difference to computer values within boundaries
        for j = 2:M
            % compute new value for sigma
            sigma = max([0.0, x(1)+(x(2)*S(j-1))+(x(3)*(S(j-1)^2))]);
            
            % Calculating our derivates approximated using the FD method.
            % The first two are central differences
            alpha_central = ((sigma^2)*(S(j)^2))/(((S(j)-S(j-1))*(S(j+1)-S(j-1))))-(r*S(j))/(S(j+1)-S(j-1));
            beta_central = ((sigma^2)*(S(j)^2))/(((S(j+1)-S(j))*(S(j+1)-S(j-1))))+(r*S(j))/(S(j+1)-S(j-1));
            % forward differences
            alpha_forward = ((sigma^2)*(S(j)^2))/(((S(j)-S(j-1))*(S(j+1)-S(j-1))));
            beta_forward = ((sigma^2)*(S(j)^2))/(((S(j+1)-S(j))*(S(j+1)-S(j-1))))+(r*S(j))/(S(j+1)-S(j-1));
            
            % Upstream weighting requires that both our values for beta and
            % alpha be postive or zero. As such, if our central difference
            % yields a negative result, we use the forward difference which
            % by definition will be positive
            if (alpha_central >= 0 ) && (beta_central >= 0)
                alpha = alpha_central;
                beta = beta_central;
            else 
                alpha = alpha_forward;
                beta = beta_forward;
            end
            
            % computing our value for the corresponding node (n+1, j) by
            % LVF model
            V(n+1, j) = V(n, j)*(1-(alpha+beta+r)*dtau)+alpha*dtau*V(n, j-1)+beta*dtau*V(n, j+1);
  
        end
    end
    
    % selecting the option value at starting price at t=0
    V0 = V(N, S==S0);

end
