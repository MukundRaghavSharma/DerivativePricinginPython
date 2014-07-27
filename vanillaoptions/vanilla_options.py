import random 
import math
from numpy import zeros
from scipy.stats import norm

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
        for i in xrange(0, self.number_of_paths):
            normal = random.normalvariate(0,1)
            stock_val = spot_changed * math.exp(standard_deviation * normal)
            if self.option_type.lower() == 'call':
                sum += max(stock_val - self.strike, 0.0)
            elif self.option_type.lower() == 'put':
                sum += max(self.strike - stock_val, 0.0)
        result = sum / self.number_of_paths
        result *= math.exp(-self.interest_rate * self.expiry)
        return result

    def reg_binomial_model_no_dividends(self):
        time_step = self.expiry / self.number_of_paths
        up_factor = math.exp(self.volatility * math.sqrt(self.expiry))
        down_factor = 1 / up_factor
        p = (math.exp(self.interest_rate * time_step) - down_factor) / (up_factor - down_factor)
        q = 1 - p
        discount_factor = math.exp(-self.interest_rate * time_step)
        underlying = zeros(self.number_of_paths + 1)
        option = zeros(self.number_of_paths + 1)

        underlying[0] = self.spot

        # Underlying Calculation #
        for i in xrange(1, self.number_of_paths + 1):
            for j in xrange(i, 0, -1): 
                underlying[j] = up_factor * underlying[j-1]
            underlying[0] = down_factor * underlying[0]
        
        # Option Calculation #
        # Underlying to Option for each time step
        if self.option_type.lower() == 'call':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(underlying[i] - self.strike, 0.0)
        elif self.option_type.lower() == 'put':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(self.strike - underlying[i], 0.0)
        
        # Discounted Risk Neutral Measure
        for i in xrange(0, self.number_of_paths):
            for j in xrange(0, self.number_of_paths):
                option[j] = ((p * option[j+1]) + ( q * option[j])) * discount_factor
        
        return option[0] 


    def reg_binomial_model_with_dividends(self, dividends):
        time_step = self.expiry / self.number_of_paths
        up_factor = math.exp(self.volatility * math.sqrt(self.expiry))
        down_factor = 1 / up_factor
        p = (math.exp((self.interest_rate - dividends) * time_step) - down_factor) / (up_factor - down_factor)
        q = 1 - p
        discount_factor = math.exp(-self.interest_rate * time_step)
        underlying = zeros(self.number_of_paths + 1)
        option = zeros(self.number_of_paths + 1)

        underlying[0] = self.spot

        # Underlying Calculation #
        for i in xrange(1, self.number_of_paths + 1):
            for j in xrange(i, 0, -1): 
                underlying[j] = up_factor * underlying[j-1]
            underlying[0] = down_factor * underlying[0]
        
        # Option Calculation #
        # Underlying to Option for each time step
        if self.option_type.lower() == 'call':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(underlying[i] - self.strike, 0.0)
        elif self.option_type.lower() == 'put':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(self.strike - underlying[i], 0.0)
        
        # Discounted Risk Neutral Measure
        for i in xrange(0, self.number_of_paths):
            for j in xrange(0, self.number_of_paths):
                option[j] = ((p * option[j+1]) + ( q * option[j])) * discount_factor
       
        if option[0] <= 0.0:
            return 0
        return option[0] 

    def ss_binomial_model_no_dividends(self, up_factor):
        time_step = self.expiry / self.number_of_paths
        down_factor = 1 / up_factor
        p = ((1 + (self.interest_rate) - down_factor))/(up_factor - down_factor)
        q = 1 - p
        discount_factor = 1 / (1 + self.interest_rate)
        underlying = zeros(self.number_of_paths + 1)
        option = zeros(self.number_of_paths + 1)  
        
        underlying[0] = self.spot

        # Underlying Calculation #
        for i in xrange(1, self.number_of_paths + 1):
            for j in xrange(i, 0, -1): 
                underlying[j] = up_factor * underlying[j-1]
            underlying[0] = down_factor * underlying[0]
        
        # Option Calculation #
        # Underlying to Option for each time step
        if self.option_type.lower() == 'call':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(underlying[i] - self.strike, 0.0)
        elif self.option_type.lower() == 'put':
            for i in xrange(0, self.number_of_paths + 1):
                option[i] = max(self.strike - underlying[i], 0.0)
        
        # Discounted Risk Neutral Measure
        for i in xrange(0, self.number_of_paths):
            for j in xrange(0, self.number_of_paths):
                option[j] = ((p * option[j+1]) + (q * option[j])) * discount_factor
        
        return option[0] 


    def black_scholes(self):
        d_1 = math.log(self.spot / self.strike) + ((self.interest_rate + (self.volatility * self.volatility)/2) *
                self.expiry)
        d_2 = d_1 - self.volatility * math.sqrt(self.expiry)
        if self.option_type.lower() == 'call':
            result = self.spot * norm.cdf(d_1) - self.strike * math.exp(-self.interest_rate * self.expiry) * norm.cdf(d_2)
            return result
        elif self.option_type.lower() == 'put':
            result = self.strike * math.exp(-self.interest_rate * expiry) * norm.cdf(-d_2) - self.spot * norm.cdf(-d_1)
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
    print "Monte Carlo Result: ", call.monte_carlo_pricer()
    up_factor = float(raw_input("Enter the up factor: " ))
    print "SS Binomial Model without dividends: ", call.ss_binomial_model_no_dividends(up_factor)
    print "Reg Binomial Model without dividends: ", call.reg_binomial_model_no_dividends()
    dividends = float(raw_input("Enter the dividend value: "))
    print "Reg Binomial Model with dividends: ", call.reg_binomial_model_with_dividends(dividends)
    print "Black Scholes Model: ", call.black_scholes()
        
if __name__ == '__main__':
    main()
