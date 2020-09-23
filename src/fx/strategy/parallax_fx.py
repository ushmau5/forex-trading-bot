from fx.settings import LOGGER
from fx.strategy.strategy import Strategy
from fx.trade.fibonacci_retracement import FibonacciRetracement
from fx.trade.trade import Trade


class ParallaxFXStrategy(Strategy):
    """
    ParallaxFX Bollinger Band & Stochastic Oscillator
    https://www.reddit.com/r/Forex/comments/h0iwbu/part_i_my_10_minuteday_trading_strategy/
    """

    entry_fib = '0.382'  # 0.382, 0.236
    stop_loss_fib = '0.786'  # 1, 0.786
    take_profit_fib = '-0.382'  # -1.618, -1, -0.618, -0.382

    @classmethod
    def is_valid_entry(cls, df):
        _df = df.copy()

        if len(_df) < 20:
            LOGGER.warning(f"{len(_df)} candle(s) is not enough data to run this strategy, skipping..")
            cls._update_valid_entry_column(_df, False)
            return _df, False

        if cls._check_upper_band(_df) or cls._check_lower_band(_df):
            cls._update_valid_entry_column(_df, True)
            return _df, True
        else:
            cls._update_valid_entry_column(_df, False)
            return _df, False

    @classmethod
    def _check_upper_band(cls, _df):
        setup_upper_bb = _df['Bollinger_Upper'].iloc[-2]
        setup_open = _df['Open'].iloc[-2]
        setup_close = _df['Close'].iloc[-2]
        setup_high = _df['High'].iloc[-2]
        setup_low = _df['Low'].iloc[-2]
        setup_stochastic_k = _df['Stochastic_Percent_K'].iloc[-2]
        setup_stochastic_d = _df['Stochastic_Percent_D'].iloc[-2]

        confirm_open = _df['Open'].iloc[-1]
        confirm_close = _df['Close'].iloc[-1]
        confirm_low = _df['Low'].iloc[-1]
        confirm_high = _df['High'].iloc[-1]
        confirm_lower_bb = _df['Bollinger_Lower'].iloc[-1]


        # Setup Candle
        #  if wicks over upper band
        #  and stochastic is over top line
        if (setup_high > setup_upper_bb) and \
                (setup_stochastic_k >= 0.8 or setup_stochastic_d >= 0.8):

            fib_levels = FibonacciRetracement.get_levels(
                min_price=confirm_low, max_price=confirm_high, mode='DESCENDING')
            take_profit = fib_levels[cls.take_profit_fib]

            # Confirmation Candle
            #  has closed below the entry point (must retrace to enter)
            #  and has a lower low than previous candle
            #  and has a lower close than previous candle
            #  and TP is above the lower band
            if (confirm_close < fib_levels[cls.entry_fib]) and \
                    (confirm_low < setup_low) and \
                    (confirm_close < setup_close) and \
                    (take_profit > confirm_lower_bb):

                return True

    @classmethod
    def _check_lower_band(cls, _df):
        setup_lower_bb = _df['Bollinger_Lower'].iloc[-2]
        setup_open = _df['Open'].iloc[-2]
        setup_close = _df['Close'].iloc[-2]
        setup_high = _df['High'].iloc[-2]
        setup_low = _df['Low'].iloc[-2]
        setup_stochastic_k = _df['Stochastic_Percent_K'].iloc[-2]
        setup_stochastic_d = _df['Stochastic_Percent_D'].iloc[-2]

        confirm_open = _df['Open'].iloc[-1]
        confirm_close = _df['Close'].iloc[-1]
        confirm_low = _df['Low'].iloc[-1]
        confirm_high = _df['High'].iloc[-1]
        confirm_upper_bb = _df['Bollinger_Upper'].iloc[-1]


        # Setup Candle
        #  if wicks under lower band
        #  and stochastic is below bottom line
        if (setup_low < setup_lower_bb) and \
                (setup_stochastic_k <= 0.2 or setup_stochastic_d <= 0.2):

            fib_levels = FibonacciRetracement.get_levels(
                min_price=confirm_low, max_price=confirm_high, mode='ASCENDING')
            take_profit = fib_levels[cls.take_profit_fib]

            # Confirmation Candle
            #  has closed above the entry point (must retrace to enter)
            #  and has a higher high than previous candle
            #  and has a higher close than previous candle
            #  and TP is below the upper band
            if (confirm_close > fib_levels[cls.entry_fib]) and \
                    (confirm_high > setup_high) and \
                    (confirm_close > setup_close) and \
                    (take_profit < confirm_upper_bb):

                return True

    @classmethod
    def _update_valid_entry_column(cls, _df, boolean_value):
        if "Valid_Entry" in _df:
            _df['Valid_Entry'].iloc[-1] = boolean_value
        else:
            _df['Valid_Entry'] = False
            _df['Valid_Entry'].iloc[-1] = boolean_value

    @classmethod
    def open_trade(cls, df, pair, risk_amount):
        _df = df.copy()
        low = _df['Low'].iloc[-1]
        high = _df['High'].iloc[-1]
        open = _df['Open'].iloc[-1]
        close = _df['Close'].iloc[-1]
        date = _df['GMT_Time'].iloc[-1]

        if close >= open:
            fib_levels = FibonacciRetracement.get_levels(min_price=low, max_price=high, mode='ASCENDING')
            trade = Trade(order_type='BUY_LIMIT',
                          pair=pair,
                          entry=fib_levels[cls.entry_fib],
                          stop_loss=fib_levels[cls.stop_loss_fib],
                          take_profit=fib_levels[cls.take_profit_fib],
                          risk_amount=risk_amount,
                          date=date)
        else:
            fib_levels = FibonacciRetracement.get_levels(min_price=low, max_price=high, mode='DESCENDING')
            trade = Trade(order_type='SELL_LIMIT',
                          pair=pair,
                          entry=fib_levels[cls.entry_fib],
                          stop_loss=fib_levels[cls.stop_loss_fib],
                          take_profit=fib_levels[cls.take_profit_fib],
                          risk_amount=risk_amount,
                          date=date)
        return trade
