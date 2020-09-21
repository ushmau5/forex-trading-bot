class FibonacciRetracement:

    @classmethod
    def get_levels(cls, min_price, max_price, mode='ASCENDING'):
        levels = {}
        diff = max_price - min_price

        if mode == "ASCENDING":
            levels = {
                "1": max_price - (1 * diff),
                "0.786": max_price - (0.786 * diff),
                "0.618": max_price - (0.618 * diff),
                "0.5": max_price - (0.5 * diff),
                "0.382": max_price - (0.382 * diff),
                "0.236": max_price - (0.236 * diff),
                "0": max_price - (0 * diff),
                "-0.382": max_price - (-0.382 * diff),
                "-0.618": max_price - (-0.618 * diff),
                "-1": max_price - (-1 * diff),
                "-1.618": max_price - (-1.618 * diff),
            }

        elif mode == "DESCENDING":
            levels = {
                "1": min_price + (1 * diff),
                "0.786": min_price + (0.786 * diff),
                "0.618": min_price + (0.618 * diff),
                "0.5": min_price + (0.5 * diff),
                "0.382": min_price + (0.382 * diff),
                "0.236": min_price + (0.236 * diff),
                "0": min_price + (0 * diff),
                "-0.382": min_price + (-0.382 * diff),
                "-0.618": min_price + (-0.618 * diff),
                "-1": min_price + (-1 * diff),
                "-1.618": min_price + (-1.618 * diff),
            }

        return levels
