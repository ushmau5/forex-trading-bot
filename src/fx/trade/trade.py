from datetime import datetime

from fx.settings import DATETIME_FORMAT


class Trade:
    def __init__(self, order_type, pair, entry, stop_loss, take_profit, risk_amount, date):
        self.order_type = order_type
        self.pair = pair
        self.entry = entry
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.risk_amount = risk_amount
        self.order_date = datetime.strptime(date, DATETIME_FORMAT)
        self.open_date = None
        self.close_date = None
        self.profit = 0
        self.state = None

        if "JPY" in pair:
            pip_multiplier = 100
        else:
            pip_multiplier = 10000

        self.pips_to_stop_loss = abs(entry - stop_loss) * pip_multiplier
        self.pips_to_take_profit = abs(take_profit - entry) * pip_multiplier
        self.risk_amount = risk_amount
        self.risk_reward_ratio = self.pips_to_take_profit / self.pips_to_stop_loss

    def update_trade(self, df):
        high = df['High'].iloc[-1]
        low = df['Low'].iloc[-1]
        date = df['GMT_Time'].iloc[-1]

        current_datetime = datetime.strptime(date, DATETIME_FORMAT)

        if self.state is None:
            if not self.order_date == current_datetime:
                if low <= self.entry <= high:
                    self.open_date = current_datetime
                    self.state = 'OPEN'

        if self.state == 'OPEN':
            if not self.order_date == current_datetime:
                if low <= self.stop_loss <= high:
                    # trade hit SL
                    self.profit = -self.risk_amount
                    self.close_date = current_datetime
                    self.state = 'CLOSED'
                    return True
                if low <= self.take_profit <= high:
                    # trade hit TP
                    self.profit = self.risk_amount * self.risk_reward_ratio
                    self.close_date = current_datetime
                    self.state = 'CLOSED'
                    return True
