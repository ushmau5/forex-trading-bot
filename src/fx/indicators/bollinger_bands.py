import plotly.graph_objects as go


class BollingerBands:
    @staticmethod
    def add_to_data(df):
        _df = df.copy()

        period = 20
        std_deviation = 2

        _df = _df.drop(columns=['Moving_Average', 'Bollinger_Upper', 'Bollinger_Lower'], errors='ignore')

        # Calculate the SMA
        _df.insert(0, 'Moving_Average', _df['Close'].rolling(period).mean())

        # Calculate the upper and lower Bollinger Bands
        _df.insert(0, 'Bollinger_Upper',
                  _df['Moving_Average'] + _df['Close'].rolling(period).std() * std_deviation)

        _df.insert(0, 'Bollinger_Lower', _df['Moving_Average'] - _df['Close'].rolling(period).std() * std_deviation)

        return _df

    @staticmethod
    def add_to_plot(fig, df, row, col):
        # Plot the three lines of the Bollinger Bands indicator
        for parameter in ['Moving_Average', 'Bollinger_Lower', 'Bollinger_Upper']:
            fig.add_trace(go.Scatter(
                name=parameter,
                x=df['GMT_Time'],
                y=df[parameter],
                showlegend=True,
                line=dict(
                    color='blue',
                    width=2,
                    dash='solid'
                ),
                mode='lines',
                opacity=0.5),
                row=row, col=col)
        return fig
