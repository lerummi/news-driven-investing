import pandas


def compute_overnight_change(y: pandas.DataFrame, equity: str):
    """
    For a single equity, compute change over night by subtracting
    closing by next days opening price.
    """
    
    return pandas.DataFrame(
        zip(
            y["date"].iloc[1:].tolist(),
            y["4. close"].values[:-1] - y["1. open"].values[1:]
        ),
        columns=["date", equity]
    ).set_index("date")


def compute_stock_price_overnight_changes(y: pandas.DataFrame):
    """
    Given the stock prices from Alpha Vantage for various equities
    compute the changes overnight, serving as target for our
    predictions.
    """

    y["date"] = pandas.to_datetime(y["date"])
    for column in ["1. open", "2. high", "3. low", "4. close"]:
        y[column] = y[column].astype(float)
    y.sort_values(["equity", "date"], inplace=True)

    changes = None
    for equity in y["equity"].unique():
        yi = y.query(f"equity == '{equity}'")
        if changes is None:
            changes = compute_overnight_change(yi, equity)
        else:
            changes = changes.join(
                compute_overnight_change(yi, equity)
            )


    return changes.reset_index()
