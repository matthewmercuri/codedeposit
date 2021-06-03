% Matthew Mercuri
% MTH 600 Final
% April 24, 2021

function [F, J] = myfun(x)
    % ========== computing F ==========
    % saving observed value to vector
    V_observed = [0.3570 0.2792 0.2146 0.1747 0.1425 0.1206 0.0676];
    % corresponding strikes for options
    Ks = [0.80 0.85 0.90 0.95 1.00 1.05 1.10];
    
    V_computed = zeros(1, length(Ks));  % vector to store computed values
    % computing values for option given x (using Monte Carlo method)
    % NOTE: this takes quite a bit of time
    for i = 1:length(Ks)
        V_computed(i) = Eur_Call_LVF_MC(1, Ks(i), 0.25, 0.03, x, 10000, 100);
    end
    
    % Objective function values at x
    F = V_computed - V_observed;
    % =================================
    
    if nargout > 1 % Two output arguments
        % ========== computing J ==========
        J = zeros(length(Ks), length(x));  % create a zeros matrix to store Jacobian as we compute it
        delta_x = 0.0001;  % small value for our FD approximation
        delta_x_vector = (zeros(1, length(x)) + delta_x); % increment for FD method
        for m = 1:length(x)
            xp = x + delta_x_vector(m);
            for n = 1:length(Ks)
                F_p = Eur_Call_LVF_MC(1, Ks(n), 0.25, 0.03, xp, 10000, 100);  % compute value for F
                J(n, m) = (F_p - F(n)) / delta_x;  % apply FD approx.
            end
        end
        % =================================
    end
end
