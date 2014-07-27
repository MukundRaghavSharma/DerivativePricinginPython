import random 
import math

class VanillaOption:
    def __init__(self, option_type, expiry, strike, spot, volatility, interest_rate, number_of_paths):
        self.option_type = option_type
        self.expiry = expiry
        self.strike = strike
        self.spot = spot
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.number_of_paths = number_of_paths

    def monte_carlo_pricer(self):
        variance = self.volatility * self.volatility * self.expiry
        standard_deviation = math.sqrt(variance)
        ito_correction = -0.5 * variance
        spot_changed = self.spot * math.exp(self.interest_rate * self.expiry + ito_correction)
        sum = 0
        for i in range(0, self.number_of_paths):
            normal = random.normalvariate(0,1)
            stock_val = spot_changed * math.exp(standard_deviation * normal)
            if self.option_type.lower() == 'call':
                sum += max(stock_val - self.strike, 0.0)
            elif self.option_type.lower() == 'put':
                sum += max(self.strike - stock_val, 0.0)
        result = sum / self.number_of_paths
        result *= math.exp(-self.interest_rate * self.expiry)
        return result

def main():
    option_type = str(raw_input("Enter 'call' for call options or 'put' for put options: "))
    expiry = float(raw_input("Enter the expiry of the option: "))
    strike = float(raw_input("Enter the strike price of the option: "))
    spot = float(raw_input("Enter the spot value of the option: "))
    volatility =  float(raw_input("Enter the volatility value of the option as a rate: ")) / 100
    interest_rate = float(raw_input("Enter the risk free interest rate as a rate: ")) / 100
    number_of_paths = int(raw_input("Enter the number of paths you want to run the simulation for: "))
    call = VanillaOption(option_type, expiry, strike, spot, volatility, interest_rate, number_of_paths) 
    print "Result: ", call.monte_carlo_pricer()

if __name__ == '__main__':
    main()
