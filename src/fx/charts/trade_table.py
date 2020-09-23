import pandas as pd
import plotly.graph_objects as go

from fx.settings import ROOT_PATH


class TradeTable:
    @staticmethod
    def create(df, output_folder=None):

        df['Order_Date'] = [d.strftime('%d/%m/%y') if not pd.isnull(d) else d for d in df['Order_Date']]
        df['Open_Date'] = [d.strftime('%d/%m/%y') if not pd.isnull(d) else d for d in df['Open_Date']]
        df['Close_Date'] = [d.strftime('%d/%m/%y') if not pd.isnull(d) else d for d in df['Close_Date']]

        colours = ['rgb(237,248,177)' if result == 'WIN' else 'rgb(254,224,210)' for result in df['Result']]

        trades_fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns)),
            cells=dict(values=[df.Pair, df.Order, df.Entry, df.SL, df.Pips_To_SL, df.TP, df.Pips_To_TP,
                               df.RRR, df.Order_Date, df.Open_Date, df.Close_Date, df.Result, df.Profit, df.Balance],
                       fill_color=[colours]))
        ])
        if output_folder:
            trades_fig.write_html(f'{ROOT_PATH}/results/{output_folder}/trade_fig.html')

        return trades_fig
