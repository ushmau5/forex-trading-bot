import copy
import plotly.graph_objects as go

from fx.indicators.bollinger_bands import BollingerBands
from fx.indicators.stochastic import Stochastic
from plotly.subplots import make_subplots


class CandlestickChart:
    @staticmethod
    def create(df, title):
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)

        fig.add_trace(go.Candlestick(
            name='Candlestick',
            x=df['GMT_Time'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']),
            row=2, col=1)

        valid_trade_indexes = df.index[df['Valid_Entry']].tolist()
        fig.add_trace(go.Candlestick(
            name='Valid_Entry',
            x=[df['GMT_Time'][i] for i in valid_trade_indexes],
            open=[df['Open'][i] for i in valid_trade_indexes],
            high=[df['High'][i] for i in valid_trade_indexes],
            low=[df['Low'][i] for i in valid_trade_indexes],
            close=[df['Close'][i] for i in valid_trade_indexes],
            increasing={'line': {'color': 'yellow'}},
            decreasing={'line': {'color': 'purple'}}),
            row=2, col=1)

        fig = BollingerBands.add_to_plot(fig, df, row=2, col=1)
        fig = Stochastic.add_to_plot(fig, df, row=1, col=1)

        fig.update_layout(
            title={
                'text': title
            }
        )

        return fig
