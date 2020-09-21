from fx.charts.candlestick_chart import CandlestickChart
from fx.settings import ROOT_PATH
from fx.client.data_client import DataClient
from fx.indicators.bollinger_bands import BollingerBands
from fx.indicators.stochastic import Stochastic

from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Backtest:

    def __init__(self, data, strategy, balance, risk):
        self.output_folder = "Test_2"

        self.clients = []
        self.strategy = strategy
        self.balance = balance
        self.risk = risk
        self.trades = []
        self.wins = 0
        self.losses = 0

        for pair, file_path in data.items():
            data_client = DataClient(time_frame='D1', pair=pair, file_path=file_path, data_size_limit=50,
                                     indicators=[Stochastic, BollingerBands])
            self.clients.append(data_client)

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
                    trade.balance = self.balance
                    chart = CandlestickChart.create(client.data, title=client.pair)

                    if trade.profit > 0:
                        self.wins += 1
                        chart.write_image(f'{ROOT_PATH}/results/D1/{self.output_folder}/WIN_{trade.date}.png',
                                          width=1280, height=720)
                    else:
                        self.losses += 1
                        chart.write_image(f'{ROOT_PATH}/results/D1/{self.output_folder}/LOSS_{trade.date}.png',
                                          width=1280, height=720)

    def _check_for_entry(self, client):
        client.data, valid_trade = self.strategy.is_valid_entry(df=client.data)
        if valid_trade:
            trade = self.strategy.open_trade(client.data, client.pair, self.balance, self.risk)
            self.trades.append(trade)

    def analyse_trades(self, trades):
        data = {'Date': [],
                'Pair': [],
                'Order': [],
                'Entry': [],
                'SL': [],
                'Pips_To_SL': [],
                'TP': [],
                'Pips_To_TP': [],
                'RRR': [],
                'Result': [],
                'Profit': [],
                'Balance': []}

        for t in trades:
            converted_date = datetime.strptime(t.date, '%d.%m.%Y %H:%M:%S.%f')
            data['Date'].append(converted_date)
            data['Pair'].append(t.pair)
            data['Order'].append(t.order_type)
            data['Entry'].append(round(t.entry, 4))
            data['SL'].append(round(t.stop_loss, 4))
            data['Pips_To_SL'].append(round(t.pips_to_stop_loss, 2))
            data['TP'].append(round(t.take_profit, 4))
            data['Pips_To_TP'].append(round(t.pips_to_take_profit, 2))
            data['RRR'].append(round(t.risk_reward_ratio, 2))
            data['Result'].append('WIN' if t.profit > 0 else 'LOSS')
            data['Profit'].append(round(t.profit, 2))
            data['Balance'].append(round(t.balance, 2))

        df = pd.DataFrame(data)

        # Equity Chart
        equity_fig = px.line(df, x='Date', y="Balance")
        equity_fig.show()
        equity_fig.write_html(f'{ROOT_PATH}/results/D1/{self.output_folder}/equity_fig.html')

        # Trade List
        colours = ['rgb(237,248,177)' if result == 'WIN' else 'rgb(254,224,210)' for result in data['Result']]

        trades_fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns)),
            cells=dict(values=[df.Date, df.Pair, df.Order, df.Entry, df.SL, df.Pips_To_SL, df.TP, df.Pips_To_TP, df.RRR,
                               df.Result, df.Profit, df.Balance],
                       fill_color=[colours]))
        ])
        trades_fig.show()
        trades_fig.write_html(f'{ROOT_PATH}/results/D1/{self.output_folder}/trade_fig.html')

