class Trade:
    def __init__(self, order_type, pair, entry, stop_loss, take_profit, balance, risk, date):
        self.order_type = order_type
        self.pair = pair
        self.entry = entry
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.balance = balance
        self.risk = risk
        self.date = date
        self.profit = 0
        self.state = None

        if "JPY" in pair:
            pip_multiplier = 100
        else:
            pip_multiplier = 10000

        self.pips_to_stop_loss = abs(entry - stop_loss) * pip_multiplier
        self.pips_to_take_profit = abs(take_profit - entry) * pip_multiplier
        self.position_size = balance * risk
        self.risk_per_pip = self.position_size / self.pips_to_stop_loss
        self.risk_reward_ratio = self.pips_to_take_profit / self.pips_to_stop_loss

    def update_trade(self, df):
        ask_high = df['High'].iloc[-1]
        ask_low = df['Low'].iloc[-1]
        current_date = df['GMT_Time'].iloc[-1]

        if self.state is None:
            if not self.date == current_date: # think trades were opening straght away! seriously needs to get some test written asap
                if ask_low <= self.entry <= ask_high:
                    self.state = 'OPEN'

        if self.state == 'OPEN':
            # Should do it like this for now which takes worst case scenario which will give under realistic results
            if not self.date == current_date:
                if ask_low <= self.stop_loss <= ask_high:
                    self.profit = -self.pips_to_stop_loss * self.risk_per_pip
                    self.state = 'CLOSED'
                    return True
                if ask_low <= self.take_profit <= ask_high:
                    self.profit = self.pips_to_take_profit * self.risk_per_pip
                    self.state = 'CLOSED'
                    return True
