from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
import random
from openpyxl import Workbook

# CREATE EXCEL SPREADSHEET
wb = Workbook()
ws1 = wb.active
ws1.title = "Monte Carlo Sim Data"
ws1['A1'] = "Inside"
ws1['B1'] = "Outside"

# LOAD RAW SVG DATAPOINTS IN
rawsvg = "387.51 1449.51 462.51 1438.51 560.51 1395.51 616.51 1323.51 656.51 1231.51 656.51 1159.51 641.51 1093.51 596.51 1018.51 564.51 969.51 548.51 919.51 545.51 865.51 558.51 804.51 597.51 744.51 656.51 666.51 698.51 586.51 732.51 480.51 738.51 388.51 713.51 315.51 668.51 244.51 594.51 177.51 498.51 136.51 419.51 118.51 377.51 115.51 331.51 121.51 276.51 133.51 213.51 157.51 166.51 195.51 127.51 243.51 92.51 291.51 70.51 358.51 60.51 435.51 65.51 526.51 79.51 609.51 115.51 675.51 142.51 712.51 178.51 765.51 196.51 811.51 200.51 865.51 197.51 888.51 171.51 960.51 140.51 1019.51 100.51 1077.51 63.51 1141.51 45.51 1189.51 45.51 1231.51 56.51 1275.51 82.51 1320.51 110.51 1355.51 161.51 1393.51 232.51 1425.51 306.51 1445.51 354.51 1453.51"


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


# FUNCTION: CONVERT SVG TO PYTHON POLYGON
def svg_to_polygon(svg="1 1 1 20 20 20 20 1"):
    svg_split = svg.split()  # Splits list of numbers into a list of numbers, individually separated
    l1 = []  # Placeholder list 1
    l2 = []  # Placeholder list 2

    for z in range(len(svg_split)):  # Iterate through split up numbers in list
        if z % 2 == 0:  # Checks if the position is mod 2, hence every second number is true for this condition. All the x-coords in other terms
            l1.append(float(svg_split[z]))  # Add it to the list
        else:
            l1.append(float(svg_split[z]))  # Otherwise it must be a y-coord,
            l2.append(l1)  # So add it to the other list
            l1 = []  # Reset placeholder

    return l2  # Return list of coordinates


# FUNCTION: MONTE CARLO METHOD SIMULATION
def monte_carlo_simulation(polygon=Polygon([[1, 1], [1, 20], [20, 20], [20, 1]]), min_x=0, min_y=0, max_x=25, max_y=25,
                           sample_points=1000, draw_points=True):
    # Number of points inside polygon, total points generated, list of generated points
    inside = 0
    total = 0
    points = []

    for x in range(sample_points): # Loop for as many sample points that a required to be generated
        q, z = random.uniform(min_x, max_x), random.uniform(min_y, max_y) # Generate random point between min/max x/y coordinates
        pt = Point(q, z) # Transform x/y coordinates into actual Point object for Shapely (py library)
        if polygon.contains(pt): # Check is polygon contains the generated point (using Shapely)
            inside += 1 # Increase counter by one
            if draw_points: # If drawing points is enabled
                plt.plot(q, z, color='green', marker='o', markersize=1) # Draw point in green on plot
        else: # Otherwise
            if draw_points: # If draw points is enabled
                plt.plot(q, z, color='red', marker='o', markersize=1) # Draw point in red on plot

        points.append([q, z]) # Add point to point list

        total += 1 # Increase counter by one

    return inside, total, points # Return important counters/lists


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


polygon = Polygon(svg_to_polygon(rawsvg))
poly_box = Polygon(svg_to_polygon("785.51 1474.51 0.51 1474.51 0.51 9.51 785.51 0.51"))

GLOBAL_sample_points = 10000
GLOBAL_sim_rounds = 1

# Run Monte Carlo Simulation GLOBAL_sim_rounds times
for j in range(GLOBAL_sim_rounds):
    print("Simulation Round: " + str(j + 1))
    inside, total, points = monte_carlo_simulation(polygon, max_x=785.51, max_y=1474.51, min_x=0.51, min_y=0.51,
                                                   draw_points=False, sample_points=GLOBAL_sample_points)
    ws1['A' + str(j + 2)] = inside
    ws1['B' + str(j + 2)] = total - inside

destination_filename = f'Monte Carlo Simulation Data-SamplePoints_{GLOBAL_sample_points}-SimRounds_{GLOBAL_sim_rounds}.xlsx'

# Save Excel Spreadsheet
wb.save(filename=destination_filename)

# Plot & Print Data Points
plt.figure(figsize=(8, 15), dpi=300)
print("Plotting Data Points")
inside, total, points = monte_carlo_simulation(polygon, max_x=785.51, max_y=1474.51, min_x=0.51, min_y=0.51,
                                               draw_points=False, sample_points=GLOBAL_sample_points)
trapezoidal_method_simulation(polygon, 20)
x, y = polygon.exterior.xy
# m, n = poly_box.exterior.xy
plt.plot(x, y)
# plt.plot(m,n)

# poly_func = Polygon(generate_points_from_function())
#
# i, t, p = monte_carlo_simulation(poly_func, max_x=10, max_y=25, min_x=0, min_y=0,
#                                                    draw_points=False, sample_points=10000)
# print(i,t)
# z,q = poly_func.exterior.xy
# # plt.plot(z,q)

print()

plt.show()
# print(points)
print(inside, total - inside, total)
print("%inside: " + str((inside / total) * 100) + ", %outside: " + str(((total - inside) / total) * 100))
