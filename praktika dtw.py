from tkinter import *
import numpy as np
import random
from math import sqrt,sin,pi
from scipy.stats.stats import pearsonr
import pickle
from tkinter import messagebox

import matplotlib as mpl
import matplotlib.pyplot as plt



#Функция чтения из файла
def read(lst,lst_val,nametxt):
        with open(nametxt) as file:
                for line in file.readlines():
                        a,b=[float(i) for i in line.split()]
                        lst.append(a)
                        lst_val.append(b)

def func(a,b):
    return [sin(i) for i in np.arange(a,b,(b-a)/float(message12.get()))]
    
def func2(a,b):
    return [sin(5*i) for i in np.arange(a,b,(b-a)/float(message12.get()))]

#Функция записи в файл
def write(lst,nametxt):
        for item in lst:
            nametxt.write("%s\n" % item)
        
def draw():
    a=float(message10.get())
    b=float(message11.get())
    x_val=func(a,b)
    y_val=func2(a,b)
    x=np.arange(a,b,(b-a)/float(message12.get()))
    y=x.copy()
##    x_val=[i+2 for i in x_val]
    plt.plot(x,x_val)
    plt.plot(y,y_val, color="red")
    plt.show()


def dtw(s, n, h, m):
    if message4.get()=='' or 2<int(message4.get())<1:
         messagebox.showinfo("GUI Python", 'Введите привязку первой точки образца')
    else:
        if message5.get()==''or 3<int(message5.get())<1:
            messagebox.showinfo("GUI Python", 'Введите cжатие образца')
        else:
            if message6.get()=='' or 3<int(message6.get())<1:
                messagebox.showinfo("GUI Python", 'Введите растяжение образца')
            else:
                if message7.get()=='' or 2<int(message7.get())<1:
                    messagebox.showinfo("GUI Python", 'Введите привязку последней точки образа')
                else:
                    firstLineVariant = int(message4.get())
                    deflateVariant = int(message5.get())
                    stretchVariant = int(message6.get())
                    lastLineVariant = int(message7.get())

                    D = [[INFINITY for j in range(m)] for i in range(n)] # выделяем память под матрицу и заполняем элементы бесконечностями
                    ways = [[-1 for j in range(m)] for i in range(n)]

                    # проход по первой строке
                    for j in range(m):
                        if firstLineVariant == 1:
                            for k in range(j + 1):
                                D[0][j] += abs(s[0] - h[k])
                        else:
                            D[0][j] = abs(s[0] - h[j])

                    # проход по всаем строкам
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
def otrez(x1,y1,x2,y2,x,y):
        return (y1-y2)*x+(x1-x2)*y+(x1*y2-x2*y1)
        
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def dtw_all():
        a=float(message10.get())
        b=float(message11.get())
        values1=func2(a,b)
        values2=func(a,b)
        v1=np.arange(a,b,(b-a)/float(message12.get()))
        v2=v1.copy()
##        v1=[i+2 for i in values1]
        
        way = dtw(values1, len(values1), values2, len(values2))
        result_x=[]
        result_y=[]
        N1=int(message8.get())
        N2=int(message9.get())
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
            fig = plt.figure()   # Создание объекта Figure
##            plt.plot(values1,v1)
            plt.plot(values2,v2, color="red")

            i=0
            
            #списки для графиков по точкам соответствия 
            res_x=[]
            res_y=[]
            res_x_val=[]
            res_y_val=[]
            
            for j in range(0,len(result_x),10):
##                plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet')
                res_x.append(v1[int(result_x[j])-1])
                res_y.append(v2[int(result_y[j])-1])
                res_x_val.append(values1[int(result_x[j])-1])
                res_y_val.append(values2[int(result_y[j])-1])
            
##            plt.plot(res_x_val,res_x)
            
            res_x=[res_x[0],res_x[res_x_val.index(max(res_x_val))],res_x[-1]]
            res_x_val=[res_x_val[0],max(res_x_val),res_x_val[-1]]

            
            c=np.linspace(res_x[0],res_x[2], int(message12.get()))
            x_interp=np.interp(c,res_x,res_x_val)#новое значение x

            way2 = dtw(x_interp, len(x_interp), values2, len(values2))
            result_x2=[]
            result_y2=[]
            
            if way2 is not None:
                    # выводим путь
                    print("Way:")
                    with open("result.txt", "w") as f:
                        for k in way2:
                            i = k // len(values2)
                            j = k % len(values2)

                            print(i + 1, j + 1)
                            f.write(str(i + 1) + " " + str(j + 1) + "\n")
                   
                    read(result_x2,result_y2,"result.txt")
                    for j in range(0,len(result_x2),2):
                            if N1<=result_x[j]<=N2:
                                plt.plot((x_interp[int(result_x2[j])-1],values2[int(result_y2[j])-1]),(c[int(result_x2[j])-1],v2[int(result_y2[j])-1]),color='violet')
            else:
                    messagebox.showinfo("GUI Python", 'Путь не найден')
            print(res_x_val)
            print(res_x)
            plt.plot(res_x_val,res_x,color='black')
##            plt.plot(res_y_val,res_y, color="red")
            
            plt.show()
        else:
            messagebox.showinfo("GUI Python", 'Путь не найден')
            
def dtw_interval():

        a=float(message10.get())
        b=float(message11.get())
        values1=func(a,b)
        v2=[a,1,b]
        values2=[np.sin(5*a),np.pi/10,np.sin(5*b)]
        c1=np.linspace(a,b,200)
        values2=np.interp(c1,v2,values2)
        v2=np.arange(a,b,(b-a)/float(message12.get()))
        v1=np.arange(a,b,(b-a)/float(message12.get()))
        v2=v1.copy()
        values2=[i+5 for i in values2]
        
        way = dtw(values1, len(values1), values2, len(values2))
        result_x=[]
        result_y=[]
        #поднимем один график для удобства
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

            if message9.get()=='':
                messagebox.showinfo("GUI Python", 'Неверная левая граница')
            else:
                if message8.get()=='':
                    messagebox.showinfo("GUI Python", 'Неверная правая граница')
                else:
                    N1=int(message8.get())
                    N2=int(message9.get())
                    
                    i=0
                    fig = plt.figure()   # Создание объекта Figure
                    plt.plot(values1,v1)
                    plt.plot(values2,v2, color="red")
                    for j in range(0,len(result_x),10):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
                        if N1<=result_x[j]<=N2:
                            plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet')
                    plt.show()
        else:
            messagebox.showinfo("GUI Python", 'Путь не найден')

    
NONE = 1
LEFT = 2
UP = 4
INFINITY = 1e300 # беконечность


#создаем окно для кнопок 
tk=Tk()
tk.title("Панель управления визуализацией")

#границы графиков
message10 = StringVar()
entry_sin = Entry(textvariable=message10,width=20)
entry_sin.grid(row=0,column=1, padx=30, pady=5,sticky="w")

message11 = StringVar()
entry_sin2 = Entry(textvariable=message11,width=20)
entry_sin2.grid(row=0,column=1, padx=30, pady=5,sticky="e")

label_sin = Label(text="Введите пределы по x:",width=50)
label_sin.grid(row=0, column=0, sticky="w")

# количество точек на графике
message12 = StringVar()
entry_sin3 = Entry(textvariable=message12,width=50)
entry_sin3.grid(row=1,column=1, padx=30, pady=5)

label_sin2 = Label(text="Введите количество точек:",width=50)
label_sin2.grid(row=1, column=0, sticky="w")

btn2=Button(tk, text='Построить соответсвие алгоритмом DTW на всем графике',width=50,command=dtw_all)
btn2.grid(row=8,column=1, padx=5, pady=5, sticky="e")

#левая граница
message4 = StringVar()

dtw_entry0 = Entry(textvariable=message4,width=50)
dtw_entry0.grid(row=4,column=1, padx=5, pady=5)
dtw_label = Label(text="Введите привязку первой точки образа  "+"\n"+"1-Привязывать обязательно с первой точки исходной кривой "+"\n"+" 2-Разрешено привязывать с любой точки исходной кривой",width=50)
dtw_label.grid(row=4, column=0, sticky="w")

message5 = StringVar()

dtw_entry1 = Entry(textvariable=message5,width=50)
dtw_entry1.grid(row=5,column=1, padx=5, pady=5)
dtw_label = Label(text="Введите cжатие образца"+"\n"+"1-сжатие запрещено "+"\n"+"2-сжатие разрешено без штрафа"+"\n"+" 3-сжатие разрешено со штрафом",width=50)
dtw_label.grid(row=5, column=0, sticky="w")

message6 = StringVar()
dtw_entry2 = Entry(textvariable=message6,width=50)
dtw_entry2.grid(row=6,column=1, padx=5, pady=5)
dtw_label = Label(text="Введите растяжение образца"+"\n"+" 1-растяжение запрещено "+"\n"+"2-растяжение разрешено без штрафа"+"\n"+" 3-растяжение разрешено со штрафом",width=50)
dtw_label.grid(row=6, column=0, sticky="w")

message7 = StringVar()
dtw_entry3 = Entry(textvariable=message7,width=50)
dtw_entry3.grid(row=7,column=1, padx=5, pady=5)
dtw_label = Label(text="Введите привязку последней точки образа "+"\n"+"1-разрешено заканчиваться на любой точке исходной кривой"+"\n"+" 2-привязывать обязательно к последней точке исходной кривой",width=50)
dtw_label.grid(row=7, column=0, sticky="w")

#левая граница
message8 = StringVar()

dtw_int_entry = Entry(textvariable=message8,width=50)
dtw_int_entry.grid(row=9,column=1, padx=5, pady=5)
dtw_int_label = Label(text="Введите левую границу интервала:",width=50)
dtw_int_label.grid(row=9, column=0, sticky="w")

#правая граница
message9 = StringVar()

dtw_int_entry2 = Entry(textvariable=message9,width=50)
dtw_int_entry2.grid(row=10,column=1, padx=5, pady=5)
dtw_int_label2 = Label(text="Введите правую границу интервала:",width=50)
dtw_int_label2.grid(row=10, column=0, sticky="w")


btn3=Button(tk, text='Построить соответсвие алгоритмом DTW на заданом интервале',width=50,command=dtw_interval)
btn3.grid(row=11,column=1, padx=5, pady=5, sticky="e")


btn5=Button(tk, text='Построить кривые',width=50,command=draw)
btn5.grid(row=13,column=1, padx=5, pady=5, sticky="e")
