import numpy as np
from loader import Loader


class PortfolioEnv:

    def __init__(self, start_date=None, end_date=None):
        self.loader = Loader()
        self.historical_data = self.loader.load(start_date, end_date)
        self.n_stocks = len(self.historical_data)
        self.prices = np.zeros(self.n_stocks)
        self.shares = np.zeros(self.n_stocks)
        self.balance = 0
        self.current_row = 0
        self.end_row = 0

    def state_shape(self):
        return 2 * np.zeros(self.n_stocks) + 1,

    def action_shape(self):
        return np.zeros(self.n_stocks),

    def reset(self, start_date=None, end_date=None):
        if start_date is None:
            self.current_row = 0
        else:
            self.current_row = self.historical_data[0].index.get_loc(start_date)
        if end_date is None:
            self.end_row = self.historical_data[0].index.size - 1
        else:
            self.end_row = self.historical_data[0].index.get_loc(end_date)
        self.prices = np.array([stock['Adj Close'][self.current_row] for stock in self.historical_data])
        self.shares = np.zeros(self.n_stocks)
        self.balance = 1000000

    def get_state(self):
        return [self.balance] + self.prices + self.shares

    def is_finished(self):
        return self.current_row == self.end_row

    def step(self, action):
        action = np.array(action)
        self.balance -= self.prices.dot(action)
        self.shares += action
        self.current_row += 1
        new_prices = np.array([stock['Adj Close'][self.current_row] for stock in self.historical_data])
        reward = (new_prices - self.prices).dot(self.shares)
        self.prices = new_prices

        return self.get_state(), reward, self.is_finished(), None
