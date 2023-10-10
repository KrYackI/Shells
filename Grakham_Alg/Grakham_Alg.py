
from random import random 
from operator import itemgetter
import matplotlib.pyplot as plt

def read_file(filename):
    points = []
    file = open(filename, 'r')
    for line in file:
            point = line.split()
            points.append([float(point[0]), float(point[1])])
    file.close
    return points

def write_in_file(filename, shell):
    file = open(filename, 'w')
    for point in points:
            file.write(str(point[0]))
            file.write(" ")
            file.write(str(point[1]))
            file.write("\n")
    file.close
    return

def Graham(points):
    shell = []
    #points.sort(key = itemgetter(0, 1))
    points.sort(key = lambda x: (x[0], x[1]))
    start_p = points[0]
    shell.append(points[0])
    points.pop(0)
    while points[1][0] == start_p[0]:
        points.pop(0)
    if points[0][0] == start_p[0]:
        shell.append(points[0])
        points.pop(0)

    points = sorted(points, reverse = True, key = lambda x: (x[1] - shell[0][1]) / (x[0] - shell[0][0]))
    points.append(start_p)

    for point in points:
        parent = len(shell) - 1
        for i in range(parent, 0, -1):
            p = (shell[i][0] - shell[i - 1][0]) * (point[1] - shell[i][1])
            q = (shell[i][1] - shell[i - 1][1]) * (point[0] - shell[i][0])
            det = p - q
            if det >= 0: 
               shell.pop(i)
            else:
                break
        shell.append(point)

    return shell

def Jarvis(points):
    shell = []
    points.sort(key = lambda x: (x[0], x[1]))
    start_p = points[0]
    shell.append(points[0])
    points.pop(0)
    while points[1][0] == start_p[0]:
        points.pop(0)
    if points[0][0] == start_p[0]:
        shell.append(points[0])
        points.pop(0)
    border_p = points[len(points) - 1]

    points.append(start_p)
    i = len(shell) - 1
    f = True

    while(True):
        if (f == True):
            point = max(points, key = lambda x: (x[0] > shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        else: 
            point = max(points, key = lambda x: (x[0] <= shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        shell.append(point)
        points.remove(point)
        i = i + 1
        if (point == border_p):
            f = False
        if(point == start_p):
            break

    return shell

def FastShell(points):
    shell = []
    points.sort(key = lambda x: (x[0], x[1]))
    left_p = points[0]
    right_p = points[len(points) - 1]
    points.pop(0)
    points.pop(len(points) - 1)
    #points.sort(key = lambda x: (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19))
    points.sort(key = lambda x: (x[0], x[1]))
    shell.append(left_p)
    FShelp(left_p, right_p, points, shell)
    shell.append(right_p)
    points.reverse()
    FShelp(right_p, left_p, points, shell)
    shell.append(left_p)

    return shell
    
    shell.append(points[0])
    points.pop(0)
    while points[1][0] == start_p[0]:
        points.pop(0)
    if points[0][0] == start_p[0]:
        shell.append(points[0])
        points.pop(0)
    border_p = points[len(points) - 1]

    points.append(start_p)
    i = len(shell) - 1
    f = True

    while(True):
        if (f == True):
            point = max(points, key = lambda x: (x[0] > shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        else: 
            point = max(points, key = lambda x: (x[0] <= shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        shell.append(point)
        points.remove(point)
        i = i + 1
        if (point == border_p):
            f = False
        if(point == start_p):
            break

    return shell

def FShelp(a, b, points, shell):
    imax = 0
    l = len(points)
    if (l == 0): 
        return
    max = ((b[0] - a[0]) * (points[0][1] - a[1]) - (b[1] - a[1]) * (points[0][0] - a[0])) / (((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5)
    for i in range (0, l):
        q = (b[0] - a[0]) * (points[i][1] - a[1])
        p = (b[1] - a[1]) * (points[i][0] - a[0])
        cur_h = (q - p) / (((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5)
        if(max < cur_h or max == cur_h and abs(points[i][0] - a[0]) < abs(points[imax][0] - a[0])):
            max = cur_h
            imax = i
    if (max <= 0):
        return
    FShelp(a, points[imax], points[0:imax], shell)
    shell.append(points[imax])
    FShelp(points[imax], b, points[imax + 1: l], shell)
    #border_point = max(reverse = True, key = lambda x: (((b[0] - a[0]) * (x[1] - a[1]) - (b[1] - a[1]) * (x[0] - a[0]) / ((b[0] - a[0])**2 + (b[1] - a[1]**2))**0.5), -abs(x[0] - a[0])))


print("Options of data filling:\n 1. Read from file\n 2. Randomize n points\n 3. Type n points\n Choose ant type a number\n\n")
case = int(input())

if case == 1:
    points = read_file("text.txt")
elif case == 2:
    n = int(input("Type n\n"))
    points = []
    for i in range(0, n):
        x = random()
        y = random() * (1 - x**2)**0.5
        points.append([((random() < 0.5) * -2 + 1) * x, ((random() < 0.5) * -2 + 1) * y])
elif case == 3:
    n = int(input("Type n\n"))
    print("Type n points as x y")
    points = []
    for i in range(0, n):
        point = input().split()
        points.append([float(point[0]), float(point[1])])

copy_p = points.copy()
shell = FastShell(copy_p)
write_in_file("answer.txt", shell)
for coord in shell:
    print(coord)

x = []
x_shell = []
y = []
y_shell = []

for point in points:
    x.append(point[0])
    y.append(point[1])

for point in shell:
    x_shell.append(point[0])
    y_shell.append(point[1])


plt.style.use('_mpl-gallery')
plt.rcParams['figure.figsize'] = [16, 9]

# make data
plt.plot(x, y, 'ro', x_shell, y_shell)


plt.show()

#3 7    4 8
#8 3
#7 5
#2 8    3 9
#5 9
#1 10