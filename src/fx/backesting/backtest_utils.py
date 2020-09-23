
def get_trade_data(start_balance, trades):
    data = {'Pair': [],
            'Order': [],
            'Entry': [],
            'SL': [],
            'Pips_To_SL': [],
            'TP': [],
            'Pips_To_TP': [],
            'RRR': [],
            'Order_Date': [],
            'Open_Date': [],
            'Close_Date': [],
            'Result': [],
            'Profit': [],
            'Balance': []
            }

    for t in trades:
        data['Pair'].append(t.pair)
        data['Order'].append(t.order_type)
        data['Entry'].append(round(t.entry, 4))
        data['SL'].append(round(t.stop_loss, 4))
        data['Pips_To_SL'].append(round(t.pips_to_stop_loss, 2))
        data['TP'].append(round(t.take_profit, 4))
        data['Pips_To_TP'].append(round(t.pips_to_take_profit, 2))
        data['RRR'].append(round(t.risk_reward_ratio, 2))
        data['Order_Date'].append(t.order_date)
        data['Open_Date'].append(t.open_date)
        data['Close_Date'].append(t.close_date)
        data['Result'].append('WIN' if t.profit > 0 else 'LOSS')
        data['Profit'].append(round(t.profit, 2))
        start_balance += t.profit
        data['Balance'].append(round(start_balance, 2))

    return data