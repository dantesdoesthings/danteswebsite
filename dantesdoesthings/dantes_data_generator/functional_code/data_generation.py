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
        return generate_natural_cubic_spline_data(input_points, graph_range, num_output_vals)


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


def generate_cubic_cardinal_spline_data(input_points: list, graph_range: list,
                                        num_output_vals: int=20, tension: float=0.9,
                                        num_segments: int=50) -> list:
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


def generate_natural_cubic_spline_data(input_points: list, graph_range: list, num_output_vals: int=20, num_segments: int=20) -> list:
    """Generates data based on the input parameters.

    Creates a spline function through the input points, then gives back values that would have
    been on the resulting function.

    :param input_points: The list of points in form [[x-vals], [y-vals]] to have the data pass through.
    :param graph_range: The range of the data in form [xMin, xMax, yMin, yMax]
    :param num_output_vals: The number of points to find values for in the output.
    :param num_segments: The number of drawn segments per interval for the resulting graph.
    :return: A list of generated values in form [[x-vals], [y-vals], [drawX, drawY]]
    """
    # Preliminary setup
    x = input_points[0]
    y = input_points[1]
    input_points = np.array(input_points)
    n = len(input_points[0])

    # Find the values needed for the calculations and populate the vectors and matrices needed
    # h is a 1-d array that acts as an intermediate calculation
    # a is the coefficient matrix for the system of cubic polynomials
    # A is the solution coefficient matrix
    # B is the vector of dependant variables
    h = np.diff(x)
    a = np.matrix(np.zeros([4, n - 1]))
    a[0] = y[0:-1]
    a[3] = y[1:]
    A = np.zeros([n*2 - 2, n*2 - 2])
    B = np.zeros(n*2 - 2)
    A[0, :2] = [-2, 1]
    B[0] = -a[0, 0]
    A[-1, -2:] = [1, -2]
    B[-1] = -a[-1, -1]
    for j in range(n-2):
        A[j + 1, 2*j + 1:2*j + 3] = h[j+1], h[j]
        B[j+1] = h[j]*a[0, j + 1] + h[j+1]*a[3, j]
        A[n - 1 + j, 2*j: 2*j + 4] = h[j+1]**2, -2*h[j+1]**2, 2*h[j]**2, -h[j]**2
        B[n - 1 + j] = h[j]**2*a[0, j + 1] - h[j+1]**2*a[3, j]

    # Solve the system
    print(A)
    b = np.linalg.solve(A, B)
    # Save the solution into the coefficient matrix
    a[1] = b[::2]
    a[2] = b[1::2]

    # Get the functions
    def t(x_in, i):
        """Helper function that coverts from x to t"""
        return (x_in - x[i]) / h[i]

    def interval_func(x_in, i):
        """Finds the values of point x on interval i. Returns border values if i indicates X is outside the borders."""
        if i == -1:
            return y[0]
        elif i > n - 2:
            return y[-1]
        t1 = t(x_in, i)
        # Get the i-th set of 4 points.
        a1 = a[:, i]
        multiplier = np.matrix([(1 - t1) ** 3, 3 * t1 * (1 - t1) ** 2, 3 * (1 - t1) * t1 ** 2, t1 ** 3])
        return float(np.matmul(multiplier, a1))

    # Apply the system to generate output values
    width = graph_range[1] - graph_range[0]
    point_distance = width / (num_output_vals + 1)
    x_output = np.arange(graph_range[0] + point_distance, graph_range[0] + width, point_distance)[:num_output_vals]
    x_locations = np.digitize(x_output, x) - 1
    y_output = np.array([interval_func(x_output[j], x_locations[j]) for j in range(len(x_output))])

    draw_x = np.concatenate(
        [[graph_range[0]]] +
        [np.arange(0, 1 + 1/num_segments, 1/num_segments) * (x[i+1] - x[i]) + x[i] for i in range(n-1)] +
        [[graph_range[1]]])
    x_draw_locations = np.digitize(draw_x, x) - 1
    draw_y = np.array([interval_func(draw_x[j], x_draw_locations[j]) for j in range(len(draw_x))])

    return [x_output, y_output, np.array([draw_x, draw_y])]


if __name__ == '__main__':
    test_input = [[10, 20, 35, 40, 50, 60], [20, 21, 20, 21, 20, 21]]
    #test_input = [[0.9, 1.3, 1.9, 2.1], [1.3, 1.5, 1.85, 2.1]]
    # test_input = [
    #     [0.5, 13.045454545454547, 30.13636363636364, 54.68181818181819, 75.22727272727273, 95.22727272727273],
    #     [43.714285714285715, 55.42857142857143, 55.42857142857143, 56.285714285714285, 56.285714285714285, 46.57142857142857]
    # ]
    test_input = np.array([[11.454545454545455,56.33482142857142],[13.818181818181818,52.049107142857146],[15.636363636363637,58.049107142857146],[15.818181818181817,51.191964285714285],[16.727272727272727,29.191964285714285],[17.272727272727273,50.90625],[17.272727272727273,65.47767857142858],[18.363636363636363,57.19196428571428],[19.818181818181817,52.62053571428571],[21.454545454545453,61.191964285714285],[23.454545454545457,70.90625],[25.636363636363633,67.47767857142857],[27.454545454545453,60.33482142857143],[27.636363636363637,19.763392857142854],[27.81818181818182,48.33482142857143],[28.909090909090907,60.620535714285715],[29.818181818181817,65.47767857142858],[30.181818181818183,67.19196428571429],[33.63636363636363,63.763392857142854],[35.63636363636364,80.33482142857142],[37.63636363636363,76.04910714285714],[38.72727272727273,70.33482142857143],[39.09090909090909,44.04910714285714],[41.27272727272727,40.90625],[43.27272727272727,49.47767857142858],[47.81818181818182,50.62053571428572],[54.72727272727273,31.191964285714285],[59.27272727272728,41.47767857142857],[62.54545454545455,83.19196428571428],[65.27272727272727,69.19196428571428],[69.45454545454545,50.62053571428572],[74.36363636363636,36.90625],[77.0909090909091,20.334821428571427],[81.63636363636364,26.620535714285715],[82.72727272727273,41.47767857142857],[82.9090909090909,60.04910714285714],[84.18181818181819,73.76339285714286],[85.63636363636363,71.19196428571428],[87.27272727272727,61.191964285714285],[90.18181818181819,58.620535714285715],[94.9090909090909,55.47767857142857]]).T
    graph_rng = [0, 70, 0, 50]
    res = np.array(generate_natural_cubic_spline_data(test_input, graph_rng, 10))
    print(res)
"""
[[11.454545454545455,56.33482142857142],[13.818181818181818,52.049107142857146],[15.636363636363637,58.049107142857146],[15.818181818181817,51.191964285714285],[16.727272727272727,29.191964285714285],[17.272727272727273,50.90625],[17.272727272727273,65.47767857142858],[18.363636363636363,57.19196428571428],[19.818181818181817,52.62053571428571],[21.454545454545453,61.191964285714285],[23.454545454545457,70.90625],[25.636363636363633,67.47767857142857],[27.454545454545453,60.33482142857143],[27.636363636363637,19.763392857142854],[27.81818181818182,48.33482142857143],[28.909090909090907,60.620535714285715],[29.818181818181817,65.47767857142858],[30.181818181818183,67.19196428571429],[33.63636363636363,63.763392857142854],[35.63636363636364,80.33482142857142],[37.63636363636363,76.04910714285714],[38.72727272727273,70.33482142857143],[39.09090909090909,44.04910714285714],[41.27272727272727,40.90625],[43.27272727272727,49.47767857142858],[47.81818181818182,50.62053571428572],[54.72727272727273,31.191964285714285],[59.27272727272728,41.47767857142857],[62.54545454545455,83.19196428571428],[65.27272727272727,69.19196428571428],[69.45454545454545,50.62053571428572],[74.36363636363636,36.90625],[77.0909090909091,20.334821428571427],[81.63636363636364,26.620535714285715],[82.72727272727273,41.47767857142857],[82.9090909090909,60.04910714285714],[84.18181818181819,73.76339285714286],[85.63636363636363,71.19196428571428],[87.27272727272727,61.191964285714285],[90.18181818181819,58.620535714285715],[94.9090909090909,55.47767857142857]]
"""