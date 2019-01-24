"""Contains code for generating data."""
import json

import numpy as np

from dantesdoesthings.utils.utils import serialize


def generate_data(input_points: list, graph_range: list, num_output_vals: int=20, style: str= 'linear') -> list:
    """Generates data based on the input parameters.

    :param input_points: The list of points in form [[x-vals], [y-vals]] to have the data pass through.
    :param graph_range: The range of the data in form [xMin, xMax, yMin, yMax]
    :param num_output_vals: The number of points to find values for in the output.
    :param style: Whether to use the 'linear' method or the 'spline' method.
    :return: A list of generated values in form [[x-vals], [y-vals]]
    """
    if style == 'linear':
        return generate_linear_data(input_points, graph_range, num_output_vals)
    elif style == 'spline':
        return generate_spline_data(input_points, graph_range, num_output_vals)


def generate_linear_data(input_points: list, graph_range: list, num_output_vals: int=20) -> list:
    """Generates data based on the input parameters.

    Creates a piecewise linear function through the input points, then gives back values that would have
    been on the resulting function.

    :param input_points: The list of points in form [[x-vals], [y-vals]] to have the data pass through.
    :param graph_range: The range of the data in form [xMin, xMax, yMin, yMax]
    :param num_output_vals: The number of points to find values for in the output.
    :return: A list of generated values in form [[x-vals], [y-vals]]
    """
    # Preliminary setup
    input_points = np.array(input_points)
    width = graph_range[1] - graph_range[0]
    point_distance = width / (num_output_vals + 1)
    x_vals = np.arange(graph_range[0] + point_distance, graph_range[0] + width, point_distance)[:num_output_vals]

    # Find the values
    y_vals = np.interp(x_vals, input_points[0], input_points[1])

    return [x_vals, y_vals]


def generate_spline_data(input_points: list, graph_range: list,
                         num_output_vals: int=20, tension: float=0.5,
                         num_segments: int=10) -> list:
    """Generates data based on the input parameters.

    Creates a spline function through the input points, then gives back values that would have
    been on the resulting function.

    :param input_points: The list of points in form [[x-vals], [y-vals]] to have the data pass through.
    :param graph_range: The range of the data in form [xMin, xMax, yMin, yMax]
    :param num_output_vals: The number of points to find values for in the output.
    :param num_segments: The number of segments in each section for the purposes of drawing.
    :param tension: Tension value for finding the spline.
    :return: A list of generated values in form [[x-vals], [y-vals]]
    """
    num_sections = len(input_points[0]) - 1
    spline_calcs = np.zeros([2, num_sections * num_segments + 1])
    # Make a copy of the input with repeated endpoints
    points = np.array([
        [input_points[0][0]] + list(input_points[0]) + [input_points[0][-1]],
        [input_points[1][0]] + list(input_points[1]) + [input_points[1][-1]]
    ], dtype=float)

    # Find tension vectors
    t1x = (points[0][2:-1] - points[0][:-3]) * tension
    t2x = (points[0][3:] - points[0][1:-2]) * tension
    t1y = (points[1][2:-1] - points[0][:-3]) * tension
    t2y = (points[1][3:] - points[0][1:-2]) * tension

    # Find values for each segment
    # Steps
    steps = np.arange(num_segments + 1) / num_segments
    steps2 = steps ** 2
    steps3 = steps ** 3

    # Cardinals
    c1 = 2 * steps3 - 3 * steps2 + 1
    c2 = -2 * steps3 + 3 * steps2
    c3 = steps3 - 2 * steps2 + steps
    c4 = steps3 - steps2
    for i in range(num_segments + 1):
        # Points
        x = c1[i] * points[0][1:-2] + c2[i] * points[0][2:-1] + c3[i] * t1x + c4[i] * t2x
        y = c1[i] * points[1][1:-2] + c2[i] * points[1][2:-1] + c3[i] * t1y + c4[i] * t2y

        # Insert values
        if i != num_segments:
            spline_calcs[0][i:-1:num_segments] = x
            spline_calcs[1][i:-1:num_segments] = y
        else:
            spline_calcs[0][i::num_segments] = x
            spline_calcs[1][i::num_segments] = y

    # Get the desired point values
    width = graph_range[1] - graph_range[0]
    point_distance = width / (num_output_vals + 1)
    x_vals = np.arange(graph_range[0] + point_distance, graph_range[0] + width, point_distance)[:num_output_vals]
    y_vals = np.interp(x_vals, spline_calcs[0], spline_calcs[1])

    return [x_vals, y_vals, spline_calcs]


def generate_spline_data2(input_points: list, graph_range: list, num_output_vals: int=20) -> list:
    """Generates data based on the input parameters.

    Creates a spline function through the input points, then gives back values that would have
    been on the resulting function.

    :param input_points: The list of points in form [[x-vals], [y-vals]] to have the data pass through.
    :param graph_range: The range of the data in form [xMin, xMax, yMin, yMax]
    :param num_output_vals: The number of points to find values for in the output.
    :return: A list of generated values in form [[x-vals], [y-vals]]
    """
    # TODO: Fix or delete because something is wrong with the calculations.
    # Preliminary setup
    x_vals = input_points[0]
    y_vals = input_points[1]
    input_points = np.array(input_points)
    num_input_points = len(input_points[0])
    width = graph_range[1] - graph_range[0]
    point_distance = width / (num_output_vals + 1)
    x_output = np.arange(graph_range[0] + point_distance, graph_range[0] + width, point_distance)[:num_output_vals]

    # Find the values
    # Perform preliminary calculations
    h_vals = np.diff(x_vals)
    print('h vals', h_vals)
    b_vals = np.diff(y_vals) / h_vals
    print('b vals', b_vals)
    v_vals = (h_vals[:-1] + h_vals[1:]) * 2
    print('v vals', v_vals)
    u_vals = np.diff(b_vals) * 6
    print('u vals', u_vals)
    # Create the system matrix that will be solved
    system_matrix = np.zeros([num_input_points - 2, num_input_points - 2])
    print('empty sys matrix', system_matrix)
    system_matrix[0][:2] = np.array([v_vals[0], h_vals[1]])
    system_matrix[-1][-2:] = np.array([h_vals[-2], v_vals[-1]])
    for i, row in enumerate(system_matrix[1:-1]):
        row[i:i + 3] = np.array([h_vals[i], v_vals[i], h_vals[i + 1]])
    print('matrix')
    print(system_matrix)
    # Solve the system
    z_vals = np.concatenate([np.array([0]), np.linalg.solve(system_matrix, u_vals), np.array([0])])
    print('z vals')
    print(z_vals)

    # Generate the functions
    piecewise_functions = []
    for p_i in range(num_input_points - 1):
        # Pre-calculate the coefficients to reduce later workload
        coeffs = [
            z_vals[p_i + 1] / (6 * h_vals[p_i]),
            z_vals[p_i] / (6 * h_vals[p_i]),
            (y_vals[p_i + 1] / h_vals[p_i] - z_vals[p_i + 1] * h_vals[p_i] / 6),
            (y_vals[p_i] / h_vals[p_i] - z_vals[p_i] * h_vals[p_i] / 6)
        ]

        # Generate the functpiece_func_numon for thpiece_func_nums sectpiece_func_numon
        def new_func(x_in):
            parts = [
                coeffs[0] * ((x_in - x_vals[p_i]) ** 3),
                coeffs[1] * ((x_vals[p_i+1] - x_in) ** 3),
                coeffs[2] * (x_in - x_vals[p_i]),
                coeffs[3] * (x_vals[p_i+1] - x_in)
            ]
            result = sum(parts)
            return result
        piecewise_functions.append(new_func)
    piecewise_functions = [piecewise_functions[0]] + piecewise_functions + [piecewise_functions[-1]]

    # Create the condition list
    x_locations = np.digitize(x_output, x_vals)
    condlist = []
    for i in range(len(piecewise_functions)):
        condlist.append(x_locations == i)

    # Calculate the output results
    y_output = np.piecewise(x_output, condlist, piecewise_functions)

    return [x_output, y_output]


if __name__ == '__main__':
    #test_input = [[10, 20, 35, 40], [20, 21, 20, 21]]
    #test_input = [[0.9, 1.3, 1.9, 2.1], [1.3, 1.5, 1.85, 2.1]]
    test_input = [
        [0.5, 13.045454545454547, 30.13636363636364, 54.68181818181819, 75.22727272727273, 95.22727272727273],
        [43.714285714285715, 55.42857142857143, 55.42857142857143, 56.285714285714285, 56.285714285714285, 46.57142857142857]
    ]
    graph_rng = [0, 80, 0, 50]
    print(np.array(generate_spline_data2(test_input, graph_rng, 10)))
