import numpy as np
import datetime as dt
import yfinance as yf



def main():
    print()
    while True:
        cp = input(f"Would you like to invest in stocks and bonds or only stocks? (B for bonds, S for no bonds) ").strip().lower()
        if cp == 'b':
            cp = 'y'
            break  
        elif cp == 's':
            cp = 'n'
            break
        else:
            print('Invalid Response')
            continue
    
    print()
    print(f'Please choose 2 stocks from the FAANG companies: \033[1mMETA, AMZN, AAPL, NFLX, GOOG\033[0m')
    stocks = list(get_stocks())

    #period of 25 years
    end = dt.datetime.now()
    start = end - dt.timedelta(days = 25*365)

    returns = get_returns(stocks, start, end)
    mean_1, mean_2 = get_mean(returns).loc[stocks[0]], get_mean(returns).loc[stocks[1]]
    std_1, std_2 = get_std(returns).loc[stocks[0]], get_std(returns).loc[stocks[1]]
    cov = get_cov(returns)
    
    #S&P 500 returns and volatility
    returns_spy = get_returns('SPY', start, end)
    mean_spy, std_spy = get_mean(returns_spy), get_std(returns_spy)
    
    #ASSUME risk-free rate is 2%
    rf = 0.02
    
    """Minimum Variance Portfolio"""
    mvp_w1, mvp_w2 = get_MVP_weight(std_1, std_2, cov)
    mvp_mean = get_portfolio_mean(mvp_w1, mvp_w2, mean_1, mean_2)
    mvp_vol = get_portfolio_volatility(mvp_w1, mvp_w2, std_1, std_2, cov)
    
    """Complete Portfolio"""
    #risky portfolio weights, mean, SD
    w1, w2 = get_tp_weights(mean_1, mean_2, std_1, std_2, rf, cov)
    mean_rp = get_portfolio_mean(w1, w2, mean_1, mean_2)
    std_rp = get_portfolio_volatility(w1, w2, std_1, std_2, cov)
    
    print()

    

    
    if cp == 'y':
        #CP weights, mean, SD
        gamma = get_risk()
        wp, wf = get_cp_weights(mean_rp, std_rp, rf, gamma)
        w1_cp, w2_cp = wp * w1, wp * w2
        mean_cp = get_portfolio_mean(wp, wf, mean_rp, rf)
        std_cp = get_portfolio_volatility(wp, wf, std_rp, 0, 0)
        
        print()
        print(f'You should allocate \033[1m{w1_cp * 100:.2f}% in {stocks[0]}, {w2_cp * 100:.2f}% in {stocks[1]}, and {wf * 100:.2f}% in Treasury Bonds\033[0m')
        print()
        
        print("Based on historical returns, this portfolio has:")
        print(f"An expected annual returns of \033[1m{mean_cp * 100:.2f}%\033[0m and a return volatility of \033[1m{std_cp * 100:.2f}%\033[0m")
        print(f"A \033[1m68% chance\033[0m of the annual returns falling \033[1mbetween {(mean_cp - std_cp) * 100:.2f}% and {(mean_cp + std_cp) * 100:.2f}%\033[0m")
        print(f"A \033[1m95% chance\033[0m of the annual returns falling \033[1mbetween {(mean_cp - std_cp * 2) * 100:.2f}% and {(mean_cp + std_cp * 2) * 100:.2f}%\033[0m")
        print()
        
        print("In comparison, the S&P 500 has:")
        print(f"An expected annual returns of \033[1m{mean_spy * 100:.2f}%\033[0m and a return volatility of \033[1m{std_spy * 100:.2f}%\033[0m")
        print(f"A \033[1m68% chance\033[0m of the annual returns falling \033[1mbetween {(mean_spy - std_spy) * 100:.2f}% and {(mean_spy + std_spy) * 100:.2f}%\033[0m")
        print(f"A \033[1m95% chance\033[0m of the annual returns falling \033[1mbetween {(mean_spy - std_spy * 2) * 100:.2f}% and {(mean_spy + std_spy * 2) * 100:.2f}%\033[0m")
        print()
        
    
    #Minimum Variance Portfolio    
    elif cp == 'n':
        print(f"For MINIMAL RISK, you should allocate \033[1m{mvp_w1*100:.2f}% in {stocks[0]} and {mvp_w2*100:.2f}% in {stocks[1]}\033[0m")
        print()
        
        print("Based on historical returns, this portfolio has:")
        print(f"An expected annual returns of \033[1m{mvp_mean * 100:.2f}%\033[0m and a return volatility of \033[1m{mvp_vol * 100:.2f}%\033[0m")
        print(f"A \033[1m68% chance\033[0m of the annual returns falling \033[1mbetween {(mvp_mean - mvp_vol) * 100:.2f}% and {(mvp_mean + mvp_vol) * 100:.2f}%\033[0m")
        print(f"A \033[1m95% chance\033[0m of the annual returns falling \033[1mbetween {(mvp_mean - mvp_vol * 2) * 100:.2f}% and {(mvp_mean + mvp_vol * 2) * 100:.2f}%\033[0m")
        print()

        print("In comparison, the S&P 500 has:")
        print(f"An expected annual returns of \033[1m{mean_spy * 100:.2f}%\033[0m and a return volatility of \033[1m{std_spy * 100:.2f}%\033[0m")
        print(f"A \033[1m68% chance\033[0m of the annual returns falling \033[1mbetween {(mean_spy - std_spy) * 100:.2f}% and {(mean_spy + std_spy) * 100:.2f}%\033[0m")
        print(f"A \033[1m95% chance\033[0m of the annual returns falling \033[1mbetween {(mean_spy - std_spy * 2) * 100:.2f}% and {(mean_spy + std_spy * 2) * 100:.2f}%\033[0m")
        print()




def get_stocks():
    faang = ['META', 'AMZN', 'AAPL', 'NFLX', 'GOOG', 'EYPT']
    while True:
        stock_1 = input('First stock: ')
        if stock_1.upper() in faang:
            stock_1 = stock_1.upper()
            break
        else:
            print('Invalid Stock')
            pass
    while True:
        stock_2 = input('Second stock: ')
        if stock_2.upper() in faang:
            stock_2 = stock_2.upper()
            break
        else:
            print('Invalid Stock')
            pass
    return stock_1, stock_2


#get data of daily returns over 25 years
def get_returns(stocks, start, end):
    stock_data = yf.download(stocks, start = start, end = end, progress = False)
    stock_data = stock_data['Adj Close']
    returns = np.log(stock_data/ stock_data.shift(1)).dropna()
    return returns


#annualized average returns for individual stock
def get_mean(returns):
    mean_returns = returns.mean() * 252                                     
    return mean_returns

#annualized volatility for individual stock
def get_std(returns):
    std_returns = returns.std() * np.sqrt(252)                              
    return std_returns

#annualized covariance
def get_cov(returns):
    cov_matrix = returns.cov()             
    cov_matrix = cov_matrix.iloc[0,1] * 252
    return cov_matrix


#Expected portfolio returns
def get_portfolio_mean(w1, w2, m1, m2):
    port_mean = w1 * m1 + w2 * m2
    port_mean = port_mean
    return port_mean

#Expected portfolio volatilty
def get_portfolio_volatility(w1, w2, s1, s2, cov):
    port_var = w1**2 * s1**2 + w2**2 * s2**2 + 2*cov*w1*w2    #deal with negative numbers in shorting
    port_vol = np.sqrt(port_var)
    return port_vol     


"""Functions for Minimum Variance Portfolio"""
#Minimum Variance Portfolio weights
def get_MVP_weight(s1, s2, cov):
    weight_1 = (s2**2 - cov)/(s1**2 + s2**2 - 2*cov)
    weight_2 = 1 - weight_1
    return weight_1, weight_2


"""Functions for Complete Portfolio"""
#risk aversion coefficient
def get_risk():
    while True:
        try:
            gamma = int(input("On a scale of 1 to 10, how much do you DISLIKE risk (10 = I don't want any risk)? "))
            if gamma <= 0:
                print('Too small')
                continue
            elif gamma > 10:
                print('Too big')
                continue
            else:
                return gamma
        except ValueError:
            print('Not an integer')
            continue
        
#risky portfolio weights
def get_tp_weights(r1, r2, s1, s2, rf, cov):
    weight_2 = ((r2-rf) * s1**2 - (r1-rf) * cov) / ((r2-rf) * s1**2 + (r1-rf) * s2**2 - (r2-rf+r1-rf) * cov)
    weight_1 = 1 - weight_2
    return weight_1, weight_2

#complete portfolio weights
def get_cp_weights(mp, sp, rf, gamma):
    weight_p = (mp - rf)/(gamma * sp**2)
    weight_f = 1 - weight_p
    return weight_p, weight_f

                                            





if __name__ == "__main__":
    main()
