import matplotlib.pyplot as plt

NONE = 1
LEFT = 2
UP = 4
INFINITY = 1e300 # беконечность


def dtw(s, n, h, m):
    #Привязка первой точки образа
	#1-Привязывать обязательно с первой точки исходной кривой
	#2-Разрешено привязывать с любой точки исходной кривой
    firstLineVariant = int(input("Enter first line variant (1 or 2): ")) # 1 or 2
    
    #Сжатие образца
	#1-сжатие запрещено
	#2-сжатие разрешено без штрафа
	#3-сжатие разрешено со штрафом
    deflateVariant = int(input("Enter deflate variant (1, 2 or 3): ")) # 1, 2 or 3
    
    #растяжение образца
	#1-растяжение запрещено
	#2-растяжение разрешено без штрафа
	#3-растяжение разрешено со штрафом
    stretchVariant = int(input("Enter stretch variant (1, 2 or 3): ")) # 1, 2 or 3
    
    #Привязка последней точки образа
	#1-разрешено заканчиваться на любой точке исходной кривой
	#2-привязывать обязательно к последней точке исходной кривой
    lastLineVariant = int(input("Enter last line variant (1 or 2): ")) # 1 or 2

    D = [[INFINITY for j in range(m)] for i in range(n)] # выделяем память под матрицу и заполняем элементы бесконечностями
    ways = [[-1 for j in range(m)] for i in range(n)]

    # проход по первой строке
    for j in range(m):
        if firstLineVariant == 1:
            for k in range(j + 1):
                D[0][j] += abs(s[0] - h[k])
        else:
            D[0][j] = abs(s[0] - h[j])

    # проход по всем строкам
    for i in range(n - 1):
        for j in range(m - 1):
            D[i + 1][j + 1] = min(D[i + 1][j + 1], D[i][j] + abs(s[i + 1] - h[j + 1])) # наложение образца
            ways[i + 1][j + 1] = ways[i + 1][j + 1] if D[i + 1][j + 1] < D[i][j] + abs(s[i + 1] - h[j + 1]) else UP + LEFT

            # сжатие
            if deflateVariant == 1:
                D[i + 1][j] = D[i + 1][j] # сжатие запрещено
                ways[i + 1][j] = ways[i + 1][j]
            elif deflateVariant == 2:
                D[i + 1][j] = min(D[i + 1][j], D[i][j]) # сжатие разрешено без штрафа
                ways[i + 1][j] = ways[i + 1][j] if D[i + 1][j] < D[i][j] else UP
            elif deflateVariant == 3:
                D[i + 1][j] = min(D[i + 1][j], D[i][j] + abs(s[i + 1]- h[j])) # сжатие разрешено со штрафом
                ways[i + 1][j] = ways[i + 1][j] if D[i + 1][j] < D[i][j] + abs(s[i + 1] - h[j]) else UP

            # растяжение
            if stretchVariant == 1:
                D[i][j + 1] = D[i][j + 1] # растяжение запрещено
                ways[i][j + 1] = ways[i][j + 1]
            elif stretchVariant == 1:
                D[i][j + 1] = min(D[i][j + 1], D[i][j]) # растяжение разрешено без штрафа
                ways[i][j + 1] = ways[i][j + 1] if D[i][j + 1] < D[i][j] else LEFT
            elif stretchVariant == 3:
                D[i][j + 1] = min(D[i][j + 1], D[i][j] + abs(s[i] - h[j + 1])) # растяжение разрешено со штрафом
                ways[i][j + 1] = ways[i][j + 1] if D[i][j + 1] < D[i][j] + abs(s[i] - h[j + 1]) else LEFT

    # проход по последней строке
    last = n - 1

    for j in range(m - 1):
        if lastLineVariant == 1:
            D[last][j + 1] = min(D[last][j + 1], D[last][j]) # можно связать с любой точкой
            ways[last][j + 1] = ways[last][j + 1] if D[last][j + 1] < D[last][j] else LEFT
        else:
            D[last][j + 1] = min(D[last][j + 1], D[last][j] + abs(s[last] - h[j + 1])) # обязательно привязать к последней
            ways[last][j + 1] = ways[last][j + 1] if D[last][j + 1] < D[last][j] + abs(s[last] - h[j + 1]) else LEFT

    lasti = n - 1
    lastj = m - 1

    # если не требуется привязка к последней точке, то ищем минимум в последней строке
    if lastLineVariant == 1:
        lastj = 0

        for j in range(1, m):
            if D[n - 1][j] < D[n - 1][lastj]:
                lastj = j

    way = [lasti * m + lastj] # создаём массив для пути обратно и запоминаем последнюю ячейку

    if D[lasti][lastj] == INFINITY:
        return None

    # пока не дойдём до конца
    while lasti != 0:
        if ways[lasti][lastj] == LEFT:
            lastj -= 1
        elif ways[lasti][lastj] == UP:
            lasti -= 1
        elif ways[lasti][lastj] == LEFT + UP:
            lastj -= 1
            lasti -= 1

        way.append(lasti * m + lastj)

    return reversed(way)

#Функция чтения из файла
def read(lst,lst_val,nametxt):
        c=0
        with open(nametxt) as file:
                for line in file.readlines():
                        a,b=[float(i) for i in line.split()]
                        lst.append(a)
                        lst_val.append(b)
#Функция записи в файл
def write(lst,nametxt):
        for item in lst:
            nametxt.write("%s\n" % item)

values1 = [] # считываем значения из первого файла
v1=[]
v2=[]
values2 = [] # считываем значения из второго файла
read(v1,values1,"y.txt")
read(v2,values2,"x.txt")
way = dtw(values1, len(values1), values2, len(values2))
result_x=[]
result_y=[]
#поднимем один график для удобства
for i in range(len(values1)):
    values1[i]+=2
if way is not None:
    # выводим путь
    print("Way:")
    with open("result.txt", "w") as f:
        for k in way:
            i = k // len(values2)
            j = k % len(values2)

            print(i + 1, j + 1)
            f.write(str(i + 1) + " " + str(j + 1) + "\n")
   
    read(result_x,result_y,"result.txt")

    plt.plot(values1,v1)
    plt.plot(values2,v2, color="red")

    i=0
        
    for j in range(0,len(result_x),10):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
        plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet')
    plt.show()
else:
    print('No way')
    
