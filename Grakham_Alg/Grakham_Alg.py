
import time
import math
import random as rnd
from operator import itemgetter
import matplotlib.pyplot as plt

#функция, читающая координаты множества точек из файла
def read_file(filename):
    points = []
    file = open(filename, 'r')
    for line in file:
            point = line.split()
            points.append([float(point[0]), float(point[1])])
    file.close
    return points

#функция, записывающая координаты множества точек в файл
def write_in_file(filename, shell):
    file = open(filename, 'w')
    for point in shell:
            file.write(str(point[0]))
            file.write(" ")
            file.write(str(point[1]))
            file.write("\n")
    file.close
    return

#алгоритм Грэкхема
def Graham(points):
    shell = []

    #нахождение самой левой нижней точки(стартовой), добавление ее и точки с наибольшим У, лежащей с ней на однои вертикальной прямой в оболочку, если такая есть
    #points.sort(key = itemgetter(0, 1))
    points.sort(key = lambda x: (x[0], x[1]))
    start_p = points[0]
    shell.append(points[0])
    #points.pop(0)
    ind = 1
    while points[ind][0] == start_p[0]:
        ind = ind + 1
    if ind > 1:
        shell.append(points[ind - 1])
        #points.pop(0)

    l = len(points)

    #сортировка точек по полярному углу относительно стартовой точки
    points = sorted(points[ind:l], reverse = True, key = lambda x: (x[1] - shell[0][1]) / (x[0] - shell[0][0]))
    #points = sorted(points, reverse = True, key = lambda x: math.atan2((x[1] - shell[0][1]), (x[0] - shell[0][0])))
    points.append(start_p)

    #проверка положения точек относительно прямой, проходящей через уже добавленые в оболочку точки
    #если детерминант векторов (Pi-1->Pi, Pi->Pi+1) больше нуля(точка слева), убираем из оболочки последнюю добавленную точку. иначе добавляем рассматриваемую точку в оболочку
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

    #возврат построенной оболочки
    return shell

#алгоритм Джарвиса
def Jarvis(points):
    shell = []

    #нахождение самой левой нижней(стартовой) и самой правой верхней(граничной) точек, добавление ее и точки с наибольшим У, лежащей с ней на однои вертикальной прямой в оболочку, если такая есть
    start_p = min(points, key = lambda x : (x[0], x[1]))
    shell.append(start_p)
    next_p = max(points, key = lambda x: (x!=start_p, math.atan2((x[0] - start_p[0]), -(x[1] - start_p[1]))))
    shell.append(next_p)
    border_p = max(points, key = lambda x : (x[0], x[1]))
    border_i = len(points) + 1

    points.append(start_p)
    sh = len(shell) - 1
    f = True

    #нахождение точки с максимальным полярным углом относительно текущей точки
    #при движении от стартовой к граничной точке рссматриваются только точки лежащие правее текущей, при движении от граничной к стартовой - только лежащие левее 
    for k in range(0, border_i):
        prev = shell[sh]
        maxangle = -10
        for i in range(k, border_i): 
            if (f == True):
                if (points[i][0] < prev[0]):
                    continue
            else:
                if (points[i][0] > prev[0]):
                    continue
            angle = math.atan2((points[i][0] - prev[0]), -(points[i][1] - prev[1]))
            if (angle > maxangle):
                        maxangle = angle
                        t = points[i]
                        points[i] = points[k]
                        points[k] = t
        shell.append(points[k])
        sh = sh + 1
        #изменение условия
        if (shell[sh] == border_p):
           f = False
        #конец цикла
        if(shell[sh] == start_p):
           break

    #возврат построенной оболочки
    return shell

#Быстрая оболочка
def FastShell(points):
    shell = []

    #нахождение самой левой нижней(стартовой) и самой правой верхней(граничной) точек
    #points.sort(key = lambda x: (x[0], x[1]))
    left_p = min(points, key = lambda x : (x[0], x[1]))
    right_p = max(points, key = lambda x : (x[0], x[1]))
    #points.pop(0)
    #points.pop(len(points) - 1)

    #добавление точек в оболочку через вспомогательную функцию FShelp
    shell.append(left_p)
    FShelp(left_p, right_p, points, shell)
    shell.append(right_p)
    #points.reverse()
    FShelp(right_p, left_p, points, shell)
    shell.append(left_p)

    #возврат построенной оболочки
    return shell

def FShelp(a, b, points, shell):
    #функция вычисляет наиболее удаленную точку слева от прямой, проходящей через вектор ab и добавляет ее в оболочку. если таких точек нет или множество точек пустое - возвращает управление вызвавшей ее функции
    imax = 0
    l = len(points)
    if (l == 0): 
        return
    max = ((b[0] - a[0]) * (points[0][1] - a[1]) - (b[1] - a[1]) * (points[0][0] - a[0]))
    for i in range (0, l):
        q = (b[0] - a[0]) * (points[i][1] - a[1])
        p = (b[1] - a[1]) * (points[i][0] - a[0])
        cur_h = (q - p)
        if(max < cur_h or max == cur_h and abs(points[i][0] - a[0]) < abs(points[imax][0] - a[0])):
            max = cur_h
            imax = i
    if (max <= 0):
        return

    leftP = 0
    rightP = l-1
    left = []
    right = []
    i = 0
    while (i < l):

        q = (b[0] - points[imax][0]) * (points[i][1] - points[imax][1])
        p = (b[1] - points[imax][1]) * (points[i][0] - points[imax][0])
        cur_h = (q - p)
        if (cur_h > 0):
            #if (i!=rightP):
            #    t = points[i]
            #    points[i] = points[rightP]
            #    points[rightP] = t
            #rightP = rightP - 1
            right.append(points[i])
        q = (points[imax][0] - a[0]) * (points[i][1] - a[1])
        p = (points[imax][1] - a[1]) * (points[i][0] - a[0])
        cur_h = (q - p)
        if (cur_h > 0):
                #if (i!=leftP):
                #    t = points[i]
                #    points[i] = points[leftP]
                #    points[leftP] = t
                #leftP = leftP + 1
            left.append(points[i])
        i = i + 1

    #Делает то же самое, но для прямой a->Pmax
    #FShelp(a, points[imax], points[0:leftP], shell)
    FShelp(a, points[imax], left, shell)
    #добавляет в оболочку Pmax
    shell.append(points[imax])
    #Делает то же самое, но для прямой Pmax->b
    #FShelp(points[imax], b, points[rightP + 1: l], shell)
    FShelp(points[imax], b, right, shell)

def Chen(points, m):
    #
    shell = []
    Gshells = []
    n = len(points)
    r = n // m
    startp = min(points, key = lambda x: (x[0], x[1]))
    for i in range (0, r):
        Gshells[i] = Graham(points[i * m: (i + 1) * m - 1])
    
    return shell

def ProxyShell(points, k):
    #
    shell = []
    for i in range(0, 2 * k + 3):
        shell.append(0)
    left_p = min(points, key = lambda x : (x[0], x[1]))
    right_p = max(points, key = lambda x : (x[0], x[1]))
    d = (right_p[0] - left_p[0]) / k
    for point in points:
        num = math.floor((point[0] - left_p[0]) / d)
        if (point == left_p or point == right_p):
            continue
        if (shell[num + 1] == 0 or point[1] < shell[num + 1][1]):
            shell[num + 1] = point
        elif(shell[2 * k + 1 - num] == 0 or point[1] > shell[2 * k + 1 - num][1]):
            shell[2 * k + 1 - num] = point
    shell[k + 1] = right_p
    shell[0] = left_p
    shell[2 * k + 2] = left_p
    i = 0
    l = len(shell)
    while(i < l):
        if (shell[i] == 0):
            shell.pop(i)
            l = l - 1
        else:
            i = i + 1
    return shell



def bench():
    file = open("bench.txt", 'w')
    i = 1000
    while (i <= 100000):
        points = []
        for j in range(0, i):
            x = rnd.random()
            y = rnd.random()
            points.append([x, y])
        start_time = time.time()
        Graham(points)
        end_time = time.time() - start_time
        file.write(str(end_time))
        file.write(" ")
        start_time = time.time()
        Jarvis(points)
        end_time = time.time() - start_time
        file.write(str(end_time))
        file.write(" ")
        start_time = time.time()
        FastShell(points)
        end_time = time.time() - start_time
        file.write(str(end_time))
        file.write(" ")
        start_time = time.time()
        ProxyShell(points, 100)
        end_time = time.time() - start_time
        file.write(str(end_time))
        file.write(" ")
        file.write("\n")
        print(str(i))
        i = i + 1000
    file.close
    return

plt.rcParams['figure.figsize'] = [16, 9]

bench()

G = []
J = []
F = []
P = []
I = []
for i in range (0, 100):
    I.append((i + 1) * 1000)

file = open("bench.txt", 'r')
for line in file:
            point = line.split()
            G.append(float(point[0]))
            J.append(float(point[1]))
            F.append(float(point[2]))
            P.append(float(point[3]))
file.close

plt.plot(I, G, 'r', I, J, 'b', I, F, 'g', I, P, 'y')


plt.show()

print("Options of data filling:\n 1. Read from file\n 2. Randomize n points\n 3. Type n points\n Choose ant type a number\n\n")
case = int(input())

#варианты задания облочек:
#ввод из файла
if case == 1:
    points = read_file("text.txt")
#случайная генерация n точек в пределах окружности с радиусом 1
elif case == 2:
    n = int(input("Type n\n"))
    points = []
    for i in range(0, n):
        #x = rnd.normalvariate(0, 5*n)
        #y = rnd.normalvariate(0, 5*n)
        #points.append([x, y])
        #x = rnd.uniform(-n, n)
        #y = rnd.uniform(-n, n)
        #points.append([x, y])
        x = rnd.random()
        y = rnd.random() * (1 - x**2)**0.5
        points.append([((rnd.random() < 0.5) * -2 + 1) * x, ((rnd.random() < 0.5) * -2 + 1) * y])
#ручной ввод координат n точек(вводятся только координаты без любых других символов. координаты в паре отделяются пробелом, пары координат отделяются переходом на новую строку(enter))
elif case == 3:
    n = int(input("Type n\n"))
    print("Type n points as x y")
    points = []
    for i in range(0, n):
        point = input().split()
        points.append([float(point[0]), float(point[1])])

#copy_p = points.copy()

print("Options of algorithms:\n 1. Graham\n 2. Jarvis\n 3. Fast Shell\n 4. ProxyShell\n Choose ant type a number\n\n")
case = int(input())

#выбор алгоритма:
if case == 1:
    start_time = time.time()
    shell = Graham(points)
    end_time = time.time() - start_time
    print (end_time)
elif case == 2:
    start_time = time.time()
    shell = Jarvis(points)
    end_time = time.time() - start_time
    print (end_time)
elif case == 3:
    start_time = time.time()
    shell = FastShell(points)
    end_time = time.time() - start_time
    print (end_time)
elif case == 4:
    start_time = time.time()
    shell = ProxyShell(points, 100)
    end_time = time.time() - start_time
    print (end_time)

#запись оболочки в файл и ее вывод на консоль
write_in_file("answer.txt", shell)
#for coord in shell:
    #print(coord)

#визуализация оболочки
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


#plt.style.use('_mpl-gallery')


# make data
plt.plot(x, y, 'ro', x_shell, y_shell, 'bo', x_shell, y_shell)


plt.show()

#3 7    4 8
#8 3
#7 5
#2 8    3 9
#5 9
#1 10