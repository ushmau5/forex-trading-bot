import plotly.graph_objects as go


class Stochastic:
    @staticmethod
    def add_to_data(df):
        _df = df.copy()

        period = 14

        _df = _df.drop(columns=['Moving_Average', 'Stochastic_Percent_K', 'Stochastic_Percent_D',
                                'Upper_Stochastic', 'Lower_Stochastic'], errors='ignore')

        # Calculate the SMA
        _df.insert(0, 'Moving_Average', _df['Close'].rolling(period).mean())

        _df.insert(0, 'Stochastic_Percent_K', (
                (_df['Close'] - _df['Close'].rolling(period).min()) /
                (_df['Close'].rolling(period).max() - _df['Close'].rolling(period).min())
        ))

        _df.insert(0, 'Stochastic_Percent_D',
                   _df['Stochastic_Percent_K'].rolling(3).mean())

        _df.insert(0, 'Upper_Stochastic', 0.8)

        _df.insert(0, 'Lower_Stochastic', 0.2)

        return _df

    @staticmethod
    def add_to_plot(fig, df, row, col):
        for parameter, color in [
            ('Stochastic_Percent_K', 'blue'),
            ('Stochastic_Percent_D', 'red')
        ]:
            fig.add_trace(go.Scatter(
                name=parameter,
                x=df['GMT_Time'],
                y=df[parameter],
                showlegend=True,
                line=dict(
                    color=color,
                    width=2,
                    dash='solid'
                ),
                mode='lines',
                opacity=0.5),
                row=row, col=col)

        for parameter in ['Upper_Stochastic', 'Lower_Stochastic']:
            fig.add_trace(go.Line(
                name=parameter,
                x=df['GMT_Time'],
                y=df[parameter],
                showlegend=True,
                line=dict(
                    color='grey',
                    width=2,
                    dash='dash'
                ),
                mode='lines',
                opacity=0.5),
                row=row, col=col)

        return fig
