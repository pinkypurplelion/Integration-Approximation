from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
import random
import math
from openpyxl import Workbook

GLOBAL_sample_points = 10000
GLOBAL_sim_rounds = 1
GLOBAL_min_x = -3
GLOBAL_max_x = 0
GLOBAL_min_y = 0
GLOBAL_max_y = 7
GLOBAL_increment = 3/12
GLOBAL_func_name = "FUNCTION_PERIODIC"


# CREATE EXCEL SPREADSHEET
wb = Workbook()
ws1 = wb.active
ws1.title = "Monte Carlo Sim Data"
ws1['A1'] = "Inside"
ws1['B1'] = "Outside"
ws1['D1'] = f"SQUARE DIMENSIONS: {GLOBAL_max_x-GLOBAL_min_x} by {GLOBAL_max_y-GLOBAL_min_y}"


# Generate data points from function
def generate_points_from_function(left_bound = 1, right_bound=10, increment=0.1):
    points = [[left_bound, 0]]
    diff = right_bound-left_bound
    num = int(diff/increment) +1
    ysum = 0
    for i in range(num):
        x = float(format(left_bound+i*increment, '.2f'))
        try:
            # FUNCTION DEFINITION
            y = (3 * math.sin((2*(x**2)) + (6*x) - 2)) + 3
            ysum += y
            print(f'{i} & {x} & {y} \\\\')
        except ZeroDivisionError:
            y = None
        # print(y)
        pt = [x,y]
        points.append(pt)
        if y is not None:
            plt.plot(x,y, color='green', marker='o', markersize=1)
    print(ysum)
    points.append([right_bound, 0])
    return points


# FUNCTION: MONTE CARLO METHOD SIMULATION
def monte_carlo_simulation(polygon, min_x=0.0, min_y=0.0, max_x=10.0, max_y=10.0,
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


polygon = Polygon(generate_points_from_function(GLOBAL_min_x, GLOBAL_max_x, GLOBAL_increment))


# Run Monte Carlo Simulation GLOBAL_sim_rounds times
for j in range(GLOBAL_sim_rounds):
    print("Simulation Round: " + str(j + 1))
    inside, total, points = monte_carlo_simulation(polygon, max_x=GLOBAL_max_x, max_y=GLOBAL_max_y, min_x=GLOBAL_min_x, min_y=GLOBAL_min_y,
                                                   draw_points=False, sample_points=GLOBAL_sample_points)
    ws1['A' + str(j + 2)] = inside
    ws1['B' + str(j + 2)] = total - inside

destination_filename = f'Monte Carlo Simulation Data-{GLOBAL_func_name}-SamplePoints_{GLOBAL_sample_points}-SimRounds_{GLOBAL_sim_rounds}.xlsx'

# Save Excel Spreadsheet
wb.save(filename=destination_filename)

axes = plt.gca()
axes.set_xlim([GLOBAL_min_x,GLOBAL_max_x])
axes.set_ylim([GLOBAL_min_y,GLOBAL_max_y])

plt.savefig(f"{GLOBAL_func_name}-FUNCTION-PLOT")
plt.show()

axes = plt.gca()
axes.set_xlim([GLOBAL_min_x,GLOBAL_max_x])
axes.set_ylim([GLOBAL_min_y,GLOBAL_max_y])


x, y = polygon.exterior.xy
plt.plot(x, y)
plt.savefig(f"{GLOBAL_func_name}-POLYGON-PLOT")
plt.show()
# Plot & Print Data Points
# plt.figure(figsize=(8, 15), dpi=300)
print("Plotting Data Points")
inside, total, points = monte_carlo_simulation(polygon, max_x=GLOBAL_max_x, max_y=GLOBAL_max_y, min_x=GLOBAL_min_x, min_y=GLOBAL_min_y,
                                               draw_points=True, sample_points=GLOBAL_sample_points)

axes = plt.gca()
axes.set_xlim([GLOBAL_min_x,GLOBAL_max_x])
axes.set_ylim([GLOBAL_min_y,GLOBAL_max_y])


plt.plot(x, y)
plt.savefig(f"{GLOBAL_func_name}-POLYGON-AND-POINTS-PLOT")
plt.show()


# print(points)
print(inside, total - inside, total)
print("%inside: " + str((inside / total) * 100) + ", %outside: " + str(((total - inside) / total) * 100))
