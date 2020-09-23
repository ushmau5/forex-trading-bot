import plotly.express as px

from fx.settings import ROOT_PATH


class EquityChart:
    @staticmethod
    def create(df, output_folder=None):
        equity_fig = px.line(df, x='Order_Date', y="Balance")

        if output_folder:
            equity_fig.write_html(f'{ROOT_PATH}/results/{output_folder}/equity_fig.html')

        return equity_fig
