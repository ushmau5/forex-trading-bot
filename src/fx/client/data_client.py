import pandas as pd


class DataClient:
    def __init__(self, time_frame, pair, file_path, data_size_limit=100, indicators=None):
        self.time_frame = time_frame
        self.pair = pair
        self.source = pd.read_csv(file_path, chunksize=1, iterator=True)
        self.data_size_limit = data_size_limit
        self.data = None
        self.indicators = indicators

    def poll(self):
        row_df = next(self.source, None)
        if row_df is None:
            return None
        else:
            self._update_data(row_df)
            response = row_df.to_dict('records')[0]
            return response

    def _update_data(self, df):
        if self.data is None:
            self.data = df.copy()

        else:
            if not len(self.data) < self.data_size_limit:
                self.data = self.data.iloc[1:]

            self.data = self.data.append(df, ignore_index=True)

        for indicator in self.indicators:
            self.data = indicator.add_to_data(self.data)
