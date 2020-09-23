import unittest
import pandas as pd

from datetime import datetime

from fx.settings import DATETIME_FORMAT
from fx.trade.trade import Trade


class TestTrade(unittest.TestCase):
    def setUp(self):
        self.data = [
            {'GMT_Time': '27.12.2019 22:00:00.000', 'Open': 1.10995, 'High': 1.11885, 'Low': 1.10966, 'Close': 1.11781},
            {'GMT_Time': '30.12.2019 22:00:00.000', 'Open': 1.11820, 'High': 1.12209, 'Low': 1.11736, 'Close': 1.11994},
            {'GMT_Time': '31.12.2019 22:00:00.000', 'Open': 1.11995, 'High': 1.12393, 'Low': 1.11989, 'Close': 1.12154}
        ]

    def test_pip_calculations(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11925, stop_loss=1.11826, take_profit=1.12123,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        self.assertAlmostEqual(trade.risk_reward_ratio, 2.0)
        self.assertAlmostEqual(trade.pips_to_stop_loss, 9.9)
        self.assertAlmostEqual(trade.pips_to_take_profit, 19.8)

    def test_pip_calculations_JPY(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='USDJPY',
                      entry=109.170, stop_loss=108.842, take_profit=109.826,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        self.assertAlmostEqual(trade.risk_reward_ratio, 2.0)
        self.assertAlmostEqual(trade.pips_to_stop_loss, 32.8)
        self.assertAlmostEqual(trade.pips_to_take_profit, 65.6)

    def test_update_trade_opens_and_hits_tp(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11813, stop_loss=1.11632, take_profit=1.12325,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.open_date, datetime.strptime('30.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.state, 'OPEN')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.close_date, datetime.strptime('31.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.state, 'CLOSED')
        self.assertAlmostEqual(trade.risk_amount, 1.0)
        self.assertAlmostEqual(trade.risk_reward_ratio, 2.83, places=2)
        self.assertAlmostEqual(trade.profit, 2.83, places=2)

    def test_update_trade_opens_and_hits_sl(self):
        trade = Trade(order_type='SELL_LIMIT',
                      pair='EURUSD',
                      entry=1.11813, stop_loss=1.12325, take_profit=1.11632,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, 'OPEN')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, 'CLOSED')
        self.assertAlmostEqual(trade.risk_amount, 1.0)
        self.assertAlmostEqual(trade.risk_reward_ratio, 0.35, places=2)
        self.assertAlmostEqual(trade.profit, -1.0)

    def test_update_trade_does_not_open(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11663, stop_loss=1.11556, take_profit=1.12325,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)
        self.assertAlmostEqual(trade.risk_reward_ratio, 6.19, places=2)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        self.assertEqual(trade.open_date, None)
        self.assertEqual(trade.close_date, None)

    def test_update_trade_opens_and_hits_sl_same_day(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11925, stop_loss=1.11756, take_profit=1.12325,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.open_date, datetime.strptime('30.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.close_date, datetime.strptime('30.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.state, 'CLOSED')
        self.assertAlmostEqual(trade.profit, -1.0)

    def test_update_trade_opens_and_hits_tp_same_day(self):
        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11925, stop_loss=1.11657, take_profit=1.12131,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.open_date, datetime.strptime('30.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.close_date, datetime.strptime('30.12.2019 22:00:00.000', DATETIME_FORMAT))
        self.assertEqual(trade.state, 'CLOSED')
        self.assertAlmostEqual(trade.risk_reward_ratio, 0.77, places=2)
        self.assertAlmostEqual(trade.profit, 0.77, places=2)

    def test_update_trade_opens_and_hits_sl_and_tp(self):
        # if trade hits TP and SL on same candle it counts as a loss

        trade = Trade(order_type='BUY_LIMIT',
                      pair='EURUSD',
                      entry=1.11925, stop_loss=1.11826, take_profit=1.12131,
                      risk_amount=1.0,
                      date='27.12.2019 22:00:00.000')

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, None)

        trade.update_trade(pd.DataFrame([self.data.pop(0)]))
        self.assertEqual(trade.state, 'CLOSED')
        self.assertAlmostEqual(trade.profit, -1.0)




