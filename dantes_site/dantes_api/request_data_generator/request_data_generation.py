import json
import os
import typing

import numpy as np
import pandas as pd
import pydantic

from dantes_api.objects import request_data_generator_call
from dantes_api.utils import utils


def even_dist(start_time: typing.Union[int, float], end_time: typing.Union[int, float], size: int):
    """A 'distribution' of evenly spaced points."""
    time_vals = np.arange(start_time, end_time, (end_time - start_time) / size)
    return time_vals


rng = np.random.default_rng()
method_map = {
    'even': even_dist,
    'integers': rng.integers,
    'choice': rng.choice,
    'beta': rng.beta,
    'binomial': rng.binomial,
    'chisquare': rng.chisquare,
    'dirichlet': rng.dirichlet,
    'exponential': rng.exponential,
    'f': rng.f,
    'gamma': rng.gamma,
    'geometric': rng.geometric,
    'gumbel': rng.gumbel,
    'hypergeometric': rng.hypergeometric,
    'laplace': rng.laplace,
    'logistic': rng.logistic,
    'lognormal': rng.lognormal,
    'logseries': rng.logseries,
    'multinomial': rng.multinomial,
    'multivariate_hypergeometric': rng.multivariate_hypergeometric,
    'multivariate_normal': rng.multivariate_normal,
    'negative_binomial': rng.negative_binomial,
    'noncentral_chisquare': rng.noncentral_chisquare,
    'noncentral_f': rng.noncentral_f,
    'normal': rng.normal,
    'pareto': rng.pareto,
    'poisson': rng.poisson,
    'power': rng.power,
    'rayleigh': rng.rayleigh,
    'standard_cauchy': rng.standard_cauchy,
    'standard_exponential': rng.standard_exponential,
    'standard_gamma': rng.standard_gamma,
    'standard_normal': rng.standard_normal,
    'standard_t': rng.standard_t,
    'triangular': rng.triangular,
    'uniform': rng.uniform,
    'vonmises': rng.vonmises,
    'wald': rng.wald,
    'weibull': rng.weibull,
    'zipf': rng.zipf
}


def generate_raw_data(descriptions: typing.List[request_data_generator_call.RequestDataGenRawMetricSet]) -> list:
    """Generates raw data from a simple"""
    result = []

    for ms in descriptions:
        curr_ms = []
        num_points = ms.timeVals.numPoints
        time_vals = generate_values(num_points,
                                    ms.timeVals.distribution.value,
                                    ms.timeVals.distParams,
                                    True)
        for series_description in ms.metricDescriptions:
            data_vals = generate_values(
                num_points,
                series_description.dataVals.distribution.value,
                series_description.dataVals.distParams)
            curr_ms.append([
                series_description.metricName,
                time_vals,
                data_vals
            ])
        result.append(curr_ms)
    return result


def generate_values(num_points: int, distribution: str, dist_params, sort: bool = False) -> np.ndarray:
    """Generates values from a given distribution. Sorts if needed."""
    vals = method_map[distribution](*dist_params, size=num_points)
    if sort:
        vals.sort()
    return vals


def simulate_queued_data(event_times: typing.Union[list, np.ndarray],
                         processing_time: typing.Union[list, np.ndarray],
                         num_queues: int = 1) -> np.ndarray:
    """Generates new data values by simulating a queue.

    Takes in time values and processing time corresponding to events that enter a queue at the given time.
    Can simulate any positive number of queues. Returns the resulting event total times.
    """
    num_points = len(event_times)
    thread_available_times = np.ones(num_queues) * event_times[0]
    thread_available_times[0] += processing_time[0]

    event_total_times = np.ndarray(num_points)

    event_total_times[0] = processing_time[0]

    for i in range(1, num_points):
        current_time = event_times[i]
        current_process_time = processing_time[i]
        oldest_thread = thread_available_times.argmin()

        # If there is a thread that is empty at the current time, latency and processing time are the same
        if thread_available_times[oldest_thread] < current_time:
            event_total_times[i] = current_process_time
            # Thread will be busy from current time until process finishes
            thread_available_times[oldest_thread] = current_time + current_process_time
        # If there is not a thread empty, the requests latency will be the shortest wait time plus the processing time
        else:
            event_total_times[i] = thread_available_times[oldest_thread] - current_time + current_process_time
            # Thread will continue to be busy this amount of additional time
            thread_available_times[oldest_thread] += current_process_time

    return event_total_times


def aggregate_data(time_vals: typing.Union[list, np.ndarray],
                   data_vals: typing.Union[list, np.ndarray],
                   aggregation_level: typing.Union[int, float],
                   aggregation_method: typing.Union[request_data_generator_call.AggregationMethod, str]
                   ) -> typing.List[np.ndarray]:
    """Aggregates data by mean or sum to the specified level."""
    if isinstance(aggregation_method, str):
        aggregation_method = request_data_generator_call.AggregationMethod[aggregation_method]

    # Make sure that aggregation level is an integer.
    aggregation_level = int(aggregation_level)
    if aggregation_level <= 0:
        raise ValueError('Aggregation error. Aggregation level used must be a positive integer.'
                         f'Input of {aggregation_level} is not allowed.')
    # Change the time series from list to Pandas series
    adjusted_time_values = pd.to_datetime(time_vals, unit='ns')
    ts = pd.Series(data_vals, index=adjusted_time_values)

    # Adjust the values as desired
    if aggregation_method is request_data_generator_call.AggregationMethod.mean:
        ts = ts.resample(str(aggregation_level) + 'NS').mean()
    elif aggregation_method is request_data_generator_call.AggregationMethod.sum:
        ts = ts.resample(str(aggregation_level) + 'NS').sum()
        np.nan_to_num(ts, False)
    else:
        raise ValueError('Aggregation error. Method used must be "mean" or "sum". '
                         f'Input of {aggregation_method} is not allowed.')

    # Translate back into our standard format
    result = [
        np.array(ts.index.values.view(np.int64)),
        np.nan_to_num(np.array(ts))
    ]

    return result
