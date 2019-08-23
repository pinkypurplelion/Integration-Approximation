rawsvg = "0.5 114.5 38.76 64.93 71.8 47.54 127.46 38.84 244.85 61.45 244.85 95.37 318.76 137.1 374.41 171.89 424.85 138.84 430.06 93.63 471.8 59.71 492.46 0.58 563.98 16.23 590.07 101.45 688.33 143.19 722.24 167.54 735.28 213.63 743.11 287.06 743.11 345.8 0.5 353.63 0.5 114.5"

split = rawsvg.split()

l1 = []
l2 = []

for z in range(len(split)):
    # if z == 0:
    #     l1.append(float(split[z]))
    # elif z == 1:
    #     l1.append(float(split[z]))
    #     l2.append(l1)
    #     l1 = []
    if z%2 == 0:
        l1.append(float(split[z]))
    else:
        l1.append(float(split[z]))
        l2.append(l1)
        l1 = []

print(split)
print(l2)