




from typing import Optional
import numpy as np
import scipy.stats as ss 
import matplotlib.pyplot as plt

''' 
======================================================
                Parameter Description
======================================================
    S: Price,      K: Strike,
    r: rate,       q: Dividend rate
    v: Volatility, T: Time in Years. 
'''


''' 
======================================================
                Helper Functions
======================================================
'''
_d1 = lambda S, K, r, q, v, T: (
    (np.log(S/K) + (r - q + .5* (v**2))*T ) / ( v * np.sqrt(T))
)
_d2 = lambda S, K, r, q, v, T:(
    _d1(S,K,r,q,v,T) - v * np.sqrt(T)
)

''' 
======================================================
                Option Greek Functions
======================================================
price: Black-Scholes no arbitrage portfolio price of a call option  

delta: The rate of change of an option price with respect to changes in
            the underlying price. For example a delta of .6 means that the option
            price will change 60 percent of the change in the stock price.
            Delta is also the number of shares required to create a risk neutral portfolio. 

Theta: Is the rate of change of an option price (options portfolio) with respect to the 
       passage of time. 

Rho: is the rate of change in the option price relative to changes in the risk-free rate 

Vega: Is the rate of change in the option price with respect changes to in volativlity 

Gamma: Is the rate of change of an options delta with respect to changes in price 

'''

call_price = lambda S, K, r, q, v, T: (
    S * np.exp(-q * T) * ss.norm.cdf(_d1(S,K,r,q,v,T)) - 
    (K * np.exp(-r * T) * ss.norm.cdf(_d2(S,K,r,q,v,T)))
)
put_price = lambda S, K, r, q, v, T: (
    K * np.exp(-r * T) * ss.norm.cdf(-_d2(S,K,r,q,v,T)) - 
    (S * np.exp(-q * T) * ss.norm.cdf(-_d1(S,K,r,q,v,T)))
)
call_delta = lambda S, K, r, q, v, T: (
    np.exp(-q*T)*ss.norm.cdf(_d1(S,K,r,q,v,T))
)
put_delta = lambda S, K, r, q, v, T: (
    (ss.norm.cdf(_d1(S,K,r,q,v,T)) - 1) *  np.exp(-q*T)
)
call_theta = lambda S, K, r, q, v, T: (
    - ( S * np.exp(-q * T) * v * ss.norm.pdf(_d1(S,K,r,q,v,T)) ) / ( 2 * np.sqrt(T))
    - (r * K * np.exp(-r * T) * ss.norm.cdf(_d2(S,K,r,q,v,T))) 
    + (q * S * np.exp(-q * T) * ss.norm.cdf(_d1(S,K,r,q,v,T)))
)
put_theta = lambda S, K, r, q, v, T: (
    - ( S * np.exp(-q * T) * v * ss.norm.pdf(_d1(S,K,r,q,v,T)) ) / ( 2 * np.sqrt(T))
    + (r * K * np.exp(-r * T) * ss.norm.cdf(-_d2(S,K,r,q,v,T)))
    - (q * S * np.exp(-q * T) * ss.norm.cdf(-_d1(S,K,r,q,v,T)))
)
call_rho = lambda S, K, r, q, v, T: (
    K * T * np.exp(-r * T) * ss.norm.cdf(_d2(S,K,r,q,v,T)) 
)
put_rho = lambda S, K, r, q, v, T: (
    -K * T * np.exp(-r * T) * ss.norm.cdf(-_d2(S,K,r,q,v,T))
)
gamma = lambda S, K, r, q, v, T: (
    (np.exp(-q * T) * ss.norm.pdf(_d1(S,K,r,q,v,T)) ) / (S * v * np.sqrt(T))
)
vega = lambda S, K, r, q, v, T: ( 
    S * ss.norm.pdf(_d1(S,K,r,q,v,T)) * np.sqrt(T)
)

'''
===========================================
        Options Parameters
===========================================
'''

'''
ITM PUT  
''' 
S = 40.15; K = 65.25
r = .08; q =  .03
v = 0.25; T =  2.33
itm_put_params = (S,K,r,q,v,T)

'''
OTM PUT
'''
S = 55.50; K = 45.5
r = 0.06; q =  0.02
v = 0.40; T =  1.75
otm_put_params = (S,K,r,q,v,T)

'''
ITM CALL
'''
S = 75.5;  K = 50.25
r =  0.10; q =  0.02
v = 0.35;  T =  2.5 
itm_call_params = (S,K,r,q,v,T)

'''
OTM CALL
'''
S = 35.4; K = 55.25
r = 0.08; q = 0.04
v = 0.25; T = 1.5
otm_call_params = (S,K,r,q,v,T)

'''
======================================================
                    Plots
======================================================
'''


if __name__ == "__main__":
    print("hello world")

    import bs_single_script as bs
    '''
======================================================
                    Delta Plot
======================================================
might be a good idea to place the different options 
paramters into a dictionary. 
'''

    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    call_price = np.vectorize(bs.call_price)
    call_delta = np.vectorize(bs.call_delta)
    print(itm_call_params)
    S,K,r,q,v,T = itm_call_params
    option_prices = call_price(stock_prices,K,r,q,v,T)
    option_deltas = call_delta(stock_prices,K,r,q,v,T)


    '''Plot Figure'''
    plt.figure(figsize=(8,4))
    plt.plot(stock_prices, option_deltas , label = "Call")
    plt.xlabel("Stock Price")
    plt.title("Call Delta for K=50.5, r=.10, q=.02, v=.35, T= 2.5")
    plt.vlines(x = 50.5, ymin = 0 , ymax = 1, color = "black", label = "Strike")
    plt.show()

    #overlay changes in volatility
    plt.figure(figsize=(8,4))
    for vol in np.linspace(.01,.85,num = 5):
        option_deltas = call_delta(stock_prices,K,r,q,vol,T)
        plt.plot(stock_prices, option_deltas , label = f"volatility: {vol}")

    plt.title("Call Delta as Function of Price and Volatility")
    plt.vlines(x = 50.5, ymin = 0 , ymax = 1, color = "black", label = "Strike")
    plt.xlabel("Stock Price")
    plt.legend()
    plt.show() 


    '''
    ======================================================
                    Theta Plot
    ======================================================
    '''
    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    time_to_expiry = np.linspace(start = .001, stop = 4, num = 400)
    call_theta = np.vectorize(bs.call_theta)
    print(f"Current Params are: {itm_call_params}")
    S,K,r,q,v,T = itm_call_params
    option_thetas = call_theta(S,K,r,q,v,time_to_expiry)


    '''Plot Figure'''
    plt.figure(figsize=(8,4))
    plt.plot(time_to_expiry, option_thetas , label = " ITM Call")
    plt.xlabel("Time to Expiry in Years")
    plt.title("ITM Call Theta v. Time for S=75.5, K=50.5, r=.10, q=.02, v=.35")
    plt.show()

    '''Plot Theta as Function of Stirke and Time '''
    plt.figure(figsize=(8,4))
    for StockPrice in range(20,100,17):
        option_thetas = call_theta(StockPrice,K,r,q,v,time_to_expiry)
        plt.plot(time_to_expiry, option_thetas , label = f"Stock Price: {StockPrice}")
        plt.xlabel("Time to Expiry in Years")
        
    plt.title("Theta as Function of Time and Current Price")
    plt.legend()
    plt.show() 

    '''
    ======================================================
                    Gamma Plot
    ======================================================
    '''

    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    time_to_expiry = np.linspace(start = .001, stop = 4, num = 400)
    gamma_vec = np.vectorize(bs.gamma)
    print(f"Current Params are: {itm_call_params}")
    S,K,r,q,v,T = itm_call_params
    option_gammas = gamma_vec(stock_prices,K,r,q,v,T)

    plt.figure(figsize=(8,4))
    plt.plot(stock_prices, option_gammas , label = " ITM Call")
    plt.xlabel("Price of Underlying S")
    plt.ylabel("Gamma: Rate of Change in Delta")
    plt.title("Gamma as Function of Price")
    plt.vlines(x = 50.25, ymin = 0 , ymax = .030, label = "Srike Price", color = "black")
    plt.legend() 



    S,K,r,q,v,T = otm_put_params
    print(f"Current Params are: {otm_put_params}")
    option_gammas = gamma_vec(stock_prices,K,r,q,v,T)
    plt.plot(stock_prices, option_gammas , label = " OTM PUT")
    plt.xlabel("Price of Underlying S")
    plt.ylabel("Gamma: Rate of Change in Delta")
    plt.title("Gamma as Function of Price")
    plt.vlines(x = 40.25, ymin = 0 , ymax = .030, label = "Srike Price Put", color = "red")
    plt.legend() 
    plt.show()

    '''
    ======================================================
                    Vega Plot
    ======================================================
    '''

    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    time_to_expiry = np.linspace(start = .001, stop = 4, num = 400)
    volatilities = np.linspace(start = .01, stop = .99, num = 500)
    vega_vec = np.vectorize(bs.vega)
    print(f"Current Params are: {itm_call_params}")
    S,K,r,q,v,T = itm_call_params
    option_vegas = vega_vec(S,K,r,q,volatilities,T)

    plt.figure(figsize=(8,4))
    plt.plot(volatilities, option_vegas , label = " ITM Call")
    plt.xlabel("Volatility as %")
    plt.ylabel("Vega: Rate of Change in Price")
    plt.title("Vega as Function of Volatility")
    plt.legend() 
    plt.show()

    '''
    ======================================================
                    Vega as Function of Time Plot
    ======================================================
    '''
    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    time_to_expiry = np.linspace(start = .001, stop = 4, num = 400)
    volatilities = np.linspace(start = .01, stop = .99, num = 500)
    vega_vec = np.vectorize(bs.vega)
    print(f"Current Params are: {itm_call_params}")
    S,K,r,q,v,T = itm_call_params
    option_vegas = vega_vec(S,K,r,q,v,time_to_expiry)

    plt.figure(figsize=(8,4))
    plt.plot(time_to_expiry, option_vegas , label = " ITM Call")
    plt.xlabel("Time to Expiry")
    plt.ylabel("Vega: Rate of Change in Price")
    plt.title("Vega as Function of Time to Expiry")
    plt.legend() 
    plt.show()


    '''
    ======================================================
                    Rho Plot
    ======================================================
    '''

    stock_prices = np.linspace(start = 1, stop = 120, num = 400)
    time_to_expiry = np.linspace(start = .001, stop = 4, num = 400)
    volatilities = np.linspace(start = .01, stop = .99, num = 500)
    interest_rates = np.linspace(start = 0.00001, stop = .20, num = 500)
    rho_vec = np.vectorize(bs.call_rho)
    print(f"Current Params are: {itm_call_params}")
    S,K,r,q,v,T = itm_call_params
    option_rhos = rho_vec(S,K,r,interest_rates,v,T)

    plt.figure(figsize=(8,4))
    plt.plot(interest_rates, option_rhos , label = " ITM Call")
    plt.xlabel("Risk-Free Rate")
    plt.ylabel("Rate of Change in Options Price")
    plt.title("Rho as Function of Risk-Free Rate")
    plt.legend() 
    plt.show()
