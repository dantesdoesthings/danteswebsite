import json

import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest

from dantes_api.data_generator import data_generation
from dantes_api.utils import utils


def data_generator(request: HttpRequest):
    return render(request, 'dantes_data_generator/data_generator.html')


def submit_data(request: HttpRequest):
    # On POST, process the data and return a relevant response
    if request.method == 'POST':
        # Reformat the relevant request params
        request_content = json.loads(request.body)
        point_values = np.array(request_content['pointValues'], dtype=float).T
        data_range = np.array([request_content['xMin'], request_content['xMax'],
                               request_content['yMin'], request_content['yMax']], dtype=int)
        # Pass the request to the data generator
        generated_data = data_generation.generate_data(point_values,
                                                       data_range,
                                                       int(request_content['numVals']),
                                                       request_content['interp'])
        # Reformat the result per request options
        result = {}
        if request_content['style'] == 'json':
            result = {
                'data': generated_data[:2],
                'curveValues': []
            }
        elif request_content['style'] == 'csv':
            result = {
                'data': utils.convert_time_series_to_csv(generated_data[:2]),
                'curveValues': []
            }
        if len(generated_data) == 3:
            result['curveValues'] = generated_data[2].T

        response = JsonResponse(result, safe=False, json_dumps_params={'default': utils.serialize})
        print(result)
        return response
