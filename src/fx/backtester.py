from fx.backest.backtest import Backtest
from fx.settings import ROOT_PATH
from fx.strategy.parallax_fx import ParallaxFXStrategy

PAIRS = [
    'AUDCAD',
    # 'AUDCHF',
    # 'AUDJPY',
    # 'AUDNZD',
    # 'AUDUSD',
    # 'CADCHF',
    # 'CHFJPY',
    # 'EURAUD',
    # 'EURCAD',
    # 'EURCHF',
    # 'EURGBP',
    # 'EURJPY',
    # 'EURNZD',
    # 'EURUSD',
    # 'GBPAUD',
    # 'GBPCAD',
    # 'GBPCHF',
    # 'GBPJPY',
    # 'GBPNZD',
    # 'GBPUSD',
    # 'NZDCAD',
    # 'NZDCHF',
    # 'NZDJPY',
    # 'NZDUSD',
    # 'USDCAD',
    # 'USDCHF',
    # 'USDJPY'
]

D1_DATA = {p: f'{ROOT_PATH}/data/D1/{p}_Candlestick_1_D_ASK_01.01.2015-01.01.2020.csv' for p in PAIRS}

backtester = Backtest(data=D1_DATA, strategy=ParallaxFXStrategy, balance=100, risk=0.01)
trades = backtester.start()
backtester.analyse_trades(trades)
a = 0



