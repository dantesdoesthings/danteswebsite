"""Handle the JSON request and related call"""

import numpy as np

from dantes_api.data_generator import data_generation
from dantes_api.utils import utils
from dantes_api.objects.data_generator_call import DataGeneratorCall


def submit_data(data_gen_call: DataGeneratorCall):
    point_values = np.array(data_gen_call.pointValues).T
    data_range = np.array([data_gen_call.xMin, data_gen_call.xMax,
                           data_gen_call.yMin, data_gen_call.yMax], dtype=int)
    x_vals, y_vals, curve_values = data_generation.generate_data(
        point_values, data_range, int(data_gen_call.numVals), data_gen_call.interp)
    if data_gen_call.style == 'json':
        result = {
            'data': [x_vals.tolist(), y_vals.tolist()],
        }
    elif data_gen_call.style == 'csv':
        result = {
            'data': [utils.convert_time_series_to_csv([x_vals, y_vals])],
        }
    else:
        raise ValueError('Data generation call error: "style" can only be "json" or "csv". \n'
                         f'Received {data_gen_call.style} instead.')
    result['curveValues'] = curve_values.T.tolist()

    return result
