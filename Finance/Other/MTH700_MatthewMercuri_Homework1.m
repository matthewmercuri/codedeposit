%This function evaluates the arbitrage-free price of a European call
% option in the Binomial tree model
% INPUTS
% S0 : stock price at time 0
% u : up factor
% d : down factor
% T : number of periods
% r : interest rate (per period)
% K : strike price of the call
% OUTPUT
% y : price of the call at time zero
clear all
close all

btmCall(20,1.2840,0.8607,2,0.0513,22)

function y = btmCall(S0,u,d,T,r,K)
    
    stockPriceMatrix = zeros(2^T,T+1);
    payoffMatrix = zeros(2^T,T+1);
    
    stockPriceMatrix(1,1) = S0
    
    while i < T+1
        
        priceHelper(stockPriceHelper(i,:))
    
end

function p = priceHelper(stockPriceMatrix)
    
    price = x*u
    stockPriceMatrix(i+2,;)
