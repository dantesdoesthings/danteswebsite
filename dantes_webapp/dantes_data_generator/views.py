import json

import numpy as np

from django.shortcuts import render
from django.http import JsonResponse

from dantes_api.data_generator import data_generation
from dantes_webapp.utils import utils


def data_generator(request):
    return render(request, 'dantes_data_generator/data_generator.html')


def submit_data(request):
    if request.method == 'POST':
        request_content = json.loads(request.body)
        point_values = np.array(request_content['point-values'], dtype=float).T
        data_range = np.array([request_content['x-min'], request_content['x-max'],
                               request_content['y-min'], request_content['y-max']], dtype=int)
        generated_data = data_generation.generate_data(point_values,
                                                       data_range,
                                                       int(request_content['num_vals']),
                                                       request_content['interp'])
        if request_content['style'] == 'json':
            result = {
                'data': generated_data[:2],
                'curve-values': []
            }
        elif request_content['style'] == 'csv':
            result = {
                'data': utils.covert_time_series_to_csv(generated_data[:2]),
                'curve-values': []
            }
        if len(generated_data) == 3:
            result['curve-values'] = generated_data[2].T

        response = JsonResponse(result, safe=False, json_dumps_params={'default': utils.serialize})
        return response
