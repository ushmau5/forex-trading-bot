from fx.backesting.backtest_utils import get_trade_data
from fx.charts.candlestick_chart import CandlestickChart
from fx.charts.equity_chart import EquityChart
from fx.charts.trade_table import TradeTable
from fx.settings import ROOT_PATH
from fx.client.data_client import DataClient
from fx.indicators.bollinger_bands import BollingerBands
from fx.indicators.stochastic import Stochastic

import pandas as pd


class Backtest:
    def __init__(self, data, strategy, balance, risk, output_folder):
        self.clients = []
        self.strategy = strategy
        self.start_balance = balance
        self.balance = balance
        self.risk = risk
        self.output_folder = output_folder
        self.trades = []
        self.wins = 0
        self.losses = 0

        for pair, file_path in data.items():
            data_client = DataClient(time_frame='D1', pair=pair, file_path=file_path, data_size_limit=50,
                                     indicators=[Stochastic, BollingerBands])
            self.clients.append(data_client)

    @property
    def risk_amount(self):
        return self.balance * self.risk

    def start(self):
        print(f"Entry Fib: {self.strategy.entry_fib} \t "
              f"SL Fib: {self.strategy.stop_loss_fib} \t "
              f"TP Fib: {self.strategy.take_profit_fib}")

        end_of_data = False
        while not end_of_data:
            for client in self.clients:
                response = client.poll()
                if response is None:
                    end_of_data = True
                else:
                    self._check_for_entry(client)
                    self._update_trades(client)
                    result = (f"Pair: {client.time_frame}/{client.pair} \t"
                              f"Date: {response['GMT_Time']} \t "
                              f"Trades: {len(self.trades)} \t "
                              f"Wins: {self.wins} \t "
                              f"Losses: {self.losses} \t "
                              f"Balance: {self.balance}")
                    print(result)

        return self.trades

    def _update_trades(self, client):
        for trade in self.trades:
            if trade.pair == client.pair:
                trade_closed = trade.update_trade(df=client.data)

                if trade_closed:
                    self.balance += trade.profit
                    chart = CandlestickChart.create(client.data, title=client.pair)

                    if trade.profit > 0:
                        self.wins += 1
                        chart.write_image(f'{ROOT_PATH}/results/{self.output_folder}/WIN_{trade.open_date}.png',
                                          width=1280, height=720)
                    elif trade.profit < 0:
                        self.losses += 1
                        chart.write_image(f'{ROOT_PATH}/results/{self.output_folder}/LOSS_{trade.open_date}.png',
                                          width=1280, height=720)

    def _check_for_entry(self, client):
        client.data, valid_trade = self.strategy.is_valid_entry(df=client.data)
        if valid_trade:
            trade = self.strategy.open_trade(client.data, client.pair, risk_amount=self.risk_amount)
            self.trades.append(trade)

    def analyse_trades(self, trades):
        data = get_trade_data(self.start_balance, trades)
        df = pd.DataFrame(data)

        # Equity Chart
        equity_chart = EquityChart.create(df, self.output_folder)
        equity_chart.show()

        # Trade Table
        trade_table = TradeTable.create(df, self.output_folder)
        trade_table.show()

