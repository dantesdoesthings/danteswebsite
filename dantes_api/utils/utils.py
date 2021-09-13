"""Various common utility functions."""

import numpy as np
import pandas as pd


def serialize(obj):
    """Handles serializing non-standard objects into JSON."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.bool_):
        return bool(obj)

    return obj.__dict__


def covert_time_series_to_csv(time_series: list):
    """Coverts a time series to a csv-formatted string.

    :param time_series: A time series of form [[time-values], [data-values]]
    :return: A string representation of a csv file version of the time series.
    """
    # Change to a DataFrame
    df = pd.DataFrame(index=time_series[0])
    df.index.name = 'time'
    df['data'] = time_series[1]

    # Get as csv
    result = df.to_csv()

    return result
