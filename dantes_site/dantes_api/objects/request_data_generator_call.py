import typing
from enum import Enum

import numpy as np
from pydantic import BaseModel


class Distribution(Enum):
    """All valid choices for distributions in the data generation calls."""
    even = 'even'
    integers = 'integers'
    choice = 'choice'
    beta = 'beta'
    binomial = 'binomial'
    chisquare = 'chisquare'
    dirichlet = 'dirichlet'
    exponential = 'exponential'
    f = 'f'
    gamma = 'gamma'
    geometric = 'geometric'
    gumbel = 'gumbel'
    hypergeometric = 'hypergeometric'
    laplace = 'laplace'
    logistic = 'logistic'
    lognormal = 'lognormal'
    logseries = 'logseries'
    multinomial = 'multinomial'
    multivariate_hypergeometric = 'multivariate_hypergeometric'
    multivariate_normal = 'multivariate_normal'
    negative_binomial = 'negative_binomial'
    noncentral_chisquare = 'noncentral_chisquare'
    noncentral_f = 'noncentral_f'
    normal = 'normal'
    pareto = 'pareto'
    poisson = 'poisson'
    power = 'power'
    rayleigh = 'rayleigh'
    standard_cauchy = 'standard_cauchy'
    standard_exponential = 'standard_exponential'
    standard_gamma = 'standard_gamma'
    standard_normal = 'standard_normal'
    standard_t = 'standard_t'
    triangular = 'triangular'
    uniform = 'uniform'
    vonmises = 'vonmises'
    wald = 'wald'
    weibull = 'weibull'
    zipf = 'zipf'


class AggregationMethod(Enum):
    sum = 'sum'
    mean = 'mean'


class RequestDataGenRawTimeVals(BaseModel):
    """Description of how to arrange time values for a request."""
    numPoints: int
    distribution: Distribution
    distParams: typing.List[typing.Union[int, float, list]]


class RequestDataGenRawDataVals(BaseModel):
    """Description of how to arrange data values for a specific metric in a request.

    Note that this will inherit number of points from the time values description.
    """
    distribution: Distribution
    distParams: typing.List[typing.Union[int, float, list]]


class RequestDataGenRawMetricDescription(BaseModel):
    """Description of a metric's data to be generated.

    Note that this will inherit number of points from the time values description.
    """
    metricName: str
    dataVals: RequestDataGenRawDataVals


class RequestDataGenRawMetricSet(BaseModel):
    """Description of a number of metrics to generate.

    The time values will be shared between all metrics. Metrics with different time values should be
    created in separate metric sets.
    """
    timeVals: RequestDataGenRawTimeVals
    metricDescriptions: typing.List[RequestDataGenRawMetricDescription]


class RequestDataGenRawCall(BaseModel):
    """Call expected from the API for the raw data generation.

     This will have a list of descriptions to iteratively and separately use for generation.
     """
    descriptions: typing.List[RequestDataGenRawMetricSet]


class RequestDataGenQueuedCall(BaseModel):
    """Call expected from the API for the queued data generation.

    Takes data from the Raw step as input.
    """
    eventTimes: typing.List[typing.Union[int, float]]
    processingTimes: typing.List[typing.Union[int, float]]
    numQueues: int


class RequestDataGenAggregateCall(BaseModel):
    """Call expected from the API for aggregating data.

    Takes data from the Raw step as input.
    """
    timeVals: typing.List[typing.Union[int, float]]
    dataVals: typing.List[typing.Union[int, float]]
    aggregationLevel: int
    aggregationMethod: AggregationMethod
