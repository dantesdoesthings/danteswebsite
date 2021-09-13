import json
import os

import pydantic

from dantes_api.utils import utils
from dantes_api.request_data_generator import request_data_generation
from dantes_api.objects import request_data_generator_call


def main():
    payload = pydantic.parse_file_as(request_data_generator_call.RequestDataGenRawCall,
                                     os.path.join('..', '..', 'reference', 'sample_request_data_gen_initial.json'))

    result_raw = request_data_generation.generate_raw_data(payload.descriptions)
    print(json.dumps({'result': result_raw}, indent=2, default=utils.serialize))
    payload = pydantic.parse_file_as(request_data_generator_call.RequestDataGenQueuedCall,
                                     os.path.join('..', '..', 'reference', 'sample_request_data_gen_queued.json'))
    result_queued = request_data_generation.simulate_queued_data(payload.eventTimes,
                                                                 payload.processingTimes,
                                                                 payload.numQueues)
    print(json.dumps({'result': result_queued}, indent=2, default=utils.serialize))
    payload = pydantic.parse_file_as(request_data_generator_call.RequestDataGenAggregateCall,
                                     os.path.join('..', '..', 'reference', 'sample_request_data_gen_aggregate.json'))
    result_aggregate = request_data_generation.aggregate_data(payload.timeVals,
                                                              payload.dataVals,
                                                              payload.aggregationLevel,
                                                              payload.aggregationMethod)
    print(json.dumps({'result': result_aggregate}, indent=2, default=utils.serialize))


if __name__ == '__main__':
    main()
