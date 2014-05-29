import random 
import math

def MonteCarloPricerDD(expiry, strike1, strike2, spot, volatility, interest_rate, number_of_paths):
    variance = volatility * volatility * expiry
    standard_deviation = math.sqrt(variance)
    ito_correction = -0.5 * variance
    spot_changed = spot * math.exp(interest_rate * expiry + ito_correction)
    sum = 0
    for i in range(0, number_of_paths):
        normal = random.normalvariate(0,1)
        stock_val = spot_changed * math.exp(standard_deviation * normal)
        payoff = 0
        if payoff >= strike1 and payoff <= strike2:
            payoff = 1    
        sum += payoff
    result = sum / number_of_paths
    result *= math.exp(-interest_rate * expiry)
    return result

def main():
    expiry = float(raw_input("Enter the expiry of the option: "))
    strike1 = float(raw_input("Enter the first strike price i.e. the lower strike price of the option: "))
    strike2 = float(raw_input("Enter the second strike price i.e. the higher strike price of the option: "))
    spot = float(raw_input("Enter the spot value of the option: "))
    volatility =  float(raw_input("Enter the volatility value of the option: "))
    interest_rate = float(raw_input("Enter the risk free interest rate: "))
    number_of_paths = int(raw_input("Enter the number of paths you want to run the simulation for: "))
    result = MonteCarloPricerDD(expiry, strike1, strike2, spot, volatility, interest_rate, number_of_paths)
    print "The value of the Double Digital option: " , result


if __name__ == '__main__':main()
