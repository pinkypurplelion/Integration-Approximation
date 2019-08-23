from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
import random
from openpyxl import Workbook

# Generate data points from function
def generate_points_from_function(left_bound = 1, right_bound=10, increment=0.1):
    points = [[left_bound, 0]]
    diff = right_bound-left_bound
    num = int(diff/increment) +1
    for i in range(num):
        x = float(format(left_bound+i*increment, '.2f'))
        try:
            y = (50 / (2 * x))
        except ZeroDivisionError:
            y = None
        # print(y)
        pt = [x,y]
        points.append(pt)
        if y != None:
            plt.plot(x,y, color='green', marker='o', markersize=1)
    points.append([right_bound, 0])
    return points

# FUNCTION: TRAPEZOIDAL METHOD SIMULATION
def trapezoidal_method_simulation(polygon, number_of_columns=100):
    max_cord = 1453.51
    min_cord = 115.52  # 118.51 for maths, 115.51 for graphics
    vertical_difference = max_cord - min_cord
    widths = vertical_difference / number_of_columns
    heights_sum = 0

    print("Calculating Columns")
    for x in range(number_of_columns - 1):
        line = LineString([(0, max_cord - (widths * (x + 1))), (800, max_cord - (widths * (x + 1)))])
        m, n = line.xy
        plt.plot(m, n)
        try:
            intersection = list(polygon.intersection(line).coords)
            # print(number_of_columns,x,intersection)

            u = intersection[0][0]
            i = intersection[1][0]

            heights_sum += i - u
            # print(i-u, heights_sum)

        except NotImplementedError:
            print("An error was caught")
            print(number_of_columns, x, m, n)
        except:
            print("Unknown error")

    print("Final estimated area:", (widths / 2) * 2 * heights_sum)

    return widths