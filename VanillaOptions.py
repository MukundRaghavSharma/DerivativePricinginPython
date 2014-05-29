import random 
import math

def MonteCarloPricer(expiry, strike, spot, volatility, interest_rate, number_of_paths):
    variance = volatility * volatility * expiry
    standard_deviation = math.sqrt(variance)
    ito_correction = -0.5 * variance
    spot_changed = spot * math.exp(interest_rate * expiry + ito_correction)
    sum = [0,0]
    for i in range(0, number_of_paths):
        normal = random.normalvariate(0,1)
        stock_val = spot_changed * math.exp(standard_deviation * normal)
        call_payoff = max(stock_val - strike, 0.0)
        put_payoff = max(strike - stock_val, 0.0)
        sum[0] += call_payoff
        sum[1] += put_payoff
    result = [0,0]
    result[0] = sum[0] / number_of_paths
    result[1] = sum[1] / number_of_paths
    result[0] *= math.exp(-interest_rate * expiry)
    result[1] *= math.exp(-interest_rate * expiry)
    return result

def main():
    expiry = float(raw_input("Enter the expiry of the option: "))
    strike = float(raw_input("Enter the strike price of the option: "))
    spot = float(raw_input("Enter the spot value of the option: "))
    volatility =  float(raw_input("Enter the volatility value of the option: "))
    interest_rate = float(raw_input("Enter the risk free interest rate: "))
    number_of_paths = int(raw_input("Enter the number of paths you want to run the simulation for: "))
    result = MonteCarloPricer(expiry, strike, spot, volatility, interest_rate, number_of_paths)
    print "The value of the call option:  " , result[0]
    print "The value of the put option: " , result[1]


if __name__ == '__main__':main()
