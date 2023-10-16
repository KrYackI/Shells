
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
    points.pop(0)
    while points[1][0] == start_p[0]:
        points.pop(0)
    if points[0][0] == start_p[0]:
        shell.append(points[0])
        points.pop(0)

    #сортировка точек по полярному углу относительно стартовой точки
    points = sorted(points, reverse = True, key = lambda x: (x[1] - shell[0][1]) / (x[0] - shell[0][0]))
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

    #нахождение точки с максимальным полярным углом относительно текущей точки
    #при движении от стартовой к граничной точке рссматриваются только точки лежащие правее текущей, при движении от граничной к стартовой - только лежащие левее 
    while(True):
        if (f == True):
            point = max(points, key = lambda x: (x[0] > shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        else: 
            point = max(points, key = lambda x: (x[0] <= shell[i][0], (x[1] - shell[i][1]) / (x[0] - shell[i][0] if x[0] != shell[i][0] else 1e-19)))
        shell.append(point)
        points.remove(point)
        i = i + 1
        #изменение условия
        if (point == border_p):
            f = False
        #конец цикла
        if(point == start_p):
            break

    #возврат построенной оболочки
    return shell

#Быстрая оболочка
def FastShell(points):
    shell = []

    #нахождение самой левой нижней(стартовой) и самой правой верхней(граничной) точек
    points.sort(key = lambda x: (x[0], x[1]))
    left_p = points[0]
    right_p = points[len(points) - 1]
    points.pop(0)
    points.pop(len(points) - 1)

    #добавление точек в оболочку через вспомогательную функцию FShelp
    shell.append(left_p)
    FShelp(left_p, right_p, points, shell)
    shell.append(right_p)
    points.reverse()
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

    #Делает то же самое, но для прямой a->Pmax
    FShelp(a, points[imax], points[0:imax], shell)
    #добавляет в оболочку Pmax
    shell.append(points[imax])
    #Делает то же самое, но для прямой Pmax->b
    FShelp(points[imax], b, points[imax + 1: l], shell)


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

copy_p = points.copy()

print("Options of algorithms:\n 1. Graham\n 2. Jarvis\n 3. Fast Shell\n Choose ant type a number\n\n")
case = int(input())

#выбор алгоритма:
if case == 1:
    shell = Graham(copy_p)
elif case == 2:
    shell = Jarvis(copy_p)
elif case == 3:
    shell = FastShell(copy_p)

#запись оболочки в файл и ее вывод на консоль
write_in_file("answer.txt", shell)
for coord in shell:
    print(coord)

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
plt.rcParams['figure.figsize'] = [16, 9]

# make data
plt.plot(x, y, 'ro', x_shell, y_shell, 'bo', x_shell, y_shell)


plt.show()

#3 7    4 8
#8 3
#7 5
#2 8    3 9
#5 9
#1 10