from tkinter import *
import numpy as np
import random
from math import *
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
#Функция записи в файл
def write(lst,nametxt):
        for item in lst:
            nametxt.write("%s\n" % item)
            
#нахождение области допустимости
def angle(N1y,N2y,f1,f2):
        
        #получаем данные по скважинам
        dist=[]
        with open('distance_96_97_87.txt') as file:
                for line in file.readlines():
                        dist.append([abs(float(i)) for i in line.split()])
        x96,y96,z96=dist[0]
        x97,y97,z97=dist[1]
        x87,y87,z87=dist[2]
        
        #падение
##        z97+=100
        
        #расстояние между скважинами
        d1=sqrt((x96-x97)**2+(y96-y97)**2+(z96-z97)**2)
        d2=sqrt((x96-x87)**2+(y96-y87)**2+(z96-z87)**2)
        d3=sqrt((x97-x87)**2+(y97-y87)**2+(z97-z87)**2)
        if f1=='96' and f2=='97' or f1=='97' and f2=='96':
                d=d1
        elif f1=='96' and f2=='87' or f1=='87' and f2=='96':
                d=d2
        else:
                d=d3
                
        c=d*tan(5*pi/180)#сдвиг
        
        MD=[]
        Z=[]
        with open(f1+'MD.txt') as file:
                for line in file.readlines():
                        l=[float(i) for i in line.split()]
                        MD.append(l[0])
                        Z.append(abs(l[3]))
                        
        MD2=[]
        Z2=[]
        with open(f2+'MD.txt') as file:
                for line in file.readlines():
                        l=[float(i) for i in line.split()]
                        MD2.append(l[0])
                        Z2.append(abs(l[3]))
                        
        #интерполирую MD и Z
        c1=np.linspace(0,len(MD)-1, 1000)
        
        MD=np.interp(c1,[i for i in range(0,len(MD))],MD)
        Z=np.interp(c1,[i for i in range(0,len(Z))],Z)
        
        c2=np.linspace(0,len(MD2)-1, 1000)
        MD2=np.interp(c2,[i for i in range(0,len(MD2))],MD2)
        Z2=np.interp(c2,[i for i in range(0,len(Z2))],Z2)
        
        #падение
##        if f1=='97':
##                Z=[i+100 for i in Z]
##        if f2=='97':
##                Z2=[i+100 for i in Z2]
        #маркеры MD в Z
        N1MD=0
        minMDN1=float('inf')
        minMDN2=float('inf')
        indN1=0
        indN2=0
        for i in range(len(MD)):
##                print(MD[i])
                if abs(MD[i]-N1y)<minMDN1:
                   minMDN1=abs(MD[i]-N1y)
                   N1MD=MD[i]
                   indN1=i
                if abs(MD[i]-N2y)<minMDN2:
                   minMDN2=abs(MD[i]-N2y)
                   N2MD=MD[i]
                   indN2=i
                   
##        print('маркеры MD',N1MD,N2MD)
        N1y=Z[indN1]
        N2y=Z[indN2]
##        print('маркеры MD в Z',N1y,N2y)
        
        #сдвиг
        N1y-=c
        N2y+=c
##        print('Z после сдвига',N1y,N2y)
        
        #обратно в MD
        N1Z=0
        N2Z=0
        minZN1=float('inf')
        minZN2=float('inf')
        indN1=0
        indN2=0
        for i in range(len(Z2)):
                if abs(Z2[i]-N1y)<minZN1:
                   minZN1=abs(Z2[i]-N1y)
                   N1Z=Z2[i]
                   indN1=i
                if abs(Z2[i]-N2y)<minZN2:
                   minZN2=abs(Z2[i]-N2y)
                   N2Z=Z2[i]
                   indN2=i
##        print('Значения Z после сдвига на второй скважине',N1Z,N2Z)
        N1y=MD2[indN1]
        N2y=MD2[indN2]
        
##        print('Допустимый:',N1y,N2y)
        return N1y,N2y

def draw():
    x=list()#глубины
    x_val=list()#значения
    read(x,x_val,"x.txt")
    x_dict={}#хранится соответствие глубин с интервалом [0,1]
    x_interval=list()#хранятся новые глубины

    #2 
    y=list()#глубины
    y_val=list()#значения
    read(y,y_val,"y.txt")
    y_dict={}#хранится соответствие глубин с интервалом [0,1]
    y_interval=list()#хранятся новые глубины

    #поднимем один график для удобства
    for i in range(len(x_val)):
        x_val[i]+=2
    plt.plot(x_val,x)
##    plt.plot(y_val,y, color="red")
    plt.show()
    
def perebor():
    s=[['97','96','87'],['96','97','87'],['97','87','96'],['87','96','97'],['87','97','96'],['96','87','97']]
    markers={'97':[2982.6,2993.1],'96':[3012.4,3020.4],'87':[3076.8,3087]}
    for i in s:
        print(i)
        k1,k2=kor(i[0],i[1],a1=markers[i[0]][0],a2=markers[i[0]][1])
        print(k1,'\t',k2)
        k1,k2=kor(i[1],i[2],a1=k1,a2=k2)
        print(k1,'\t',k2)
        k1,k2=kor(i[2],i[0],a1=k1,a2=k2)
        print(k1,'\t',k2)
        
def kor(f1,f2,a1=0,a2=0):
        #1
        x=list()#глубины
        x_val=list()#значения
        read(x,x_val,'s'+f1+".txt")
        ##    c=np.linspace(0,len(x),500)
        ##    x=np.interp(c,[i for i in range(0,len(x))],x)
        ##    x_val=np.interp(c,[i for i in range(0,len(x_val))],x_val)

        #2 
        y=list()#глубины
        y_val=list()#значения
        read(y,y_val,'s'+f2+".txt")
        ##    c=np.linspace(0,len(y),500)
        ##    y=np.interp(c,[i for i in range(0,len(y))],y)
        ##    y_val=np.interp(c,[i for i in range(0,len(y_val))],y_val)
##        if f1=='97':
##                x=np.linspace(min(x)+2,max(x)-2,len(x))
##        elif f2=='97':
##                y=np.linspace(min(y)+2,max(y)-2,len(y))

        N1=a1
        N2=a2
        M=int(message3.get())
        minN1=float('inf')
        minN2=float('inf')
        N1_new=0
        N2_new=0
        for i in range(len(x)):
            if x[i]==N1:
                    N1_new=i
            elif minN1>abs(x[i]-N1):
                    minN1=abs(x[i]-N1)
                    N1_new=i
            if x[i]==N2:
                    N2_new=i
            elif minN2>abs(x[i]-N2):
                    minN2=abs(x[i]-N2)
                    N2_new=i
        N1=N1_new
        N2=N2_new
##        print('Приближенное к маркерам',x[N1],x[N2])
        distance=angle(x[N1],x[N2],f1,f2)

        x_dict={}#хранится соответствие глубин с интервалом [0,1]
        x_interval=list()#хранятся новые глубины


        y_dict={}#хранится соответствие глубин с интервалом [0,1]
        y_interval=list()#хранятся новые глубины

        for i in range(len(x)):
                x_dict[i*1/len(x)]=x[i]
                #изменяем глубины на интервал [0,1]
                x_interval.append(i*1/len(x))


        for i in range(len(y)):
                y_dict[i*1/len(y)]=y[i]
                #изменяем глубины на интервал [0,1]
                y_interval.append(i*1/len(y))

        #переинтерполируем на новом интервале [0,1] оба графика
        c=np.linspace(min(min(x_interval),min(y_interval)),max(max(x_interval),max(y_interval)), (len(x_interval)+len(y_interval))//2)
        x_interp=np.interp(c,x_interval,x_val)#новое значение x
        y_interp=np.interp(c,y_interval,y_val)#новое значение y

        x_interp_txt=open( "x_interp.txt", 'w' )
        y_interp_txt=open( "y_interp.txt", 'w' )

        write(x_interp,x_interp_txt)
        write(y_interp,y_interp_txt)

        #вводим границы окна и отклонение
        #N1,N2=[int(i) for i in input("Введите границы окна:").split()]
   
        fig = plt.figure()   # Создание объекта Figure
        ##                print (fig.axes)   # Список текущих областей рисования пуст
        ##                print (type(fig))   # тип объекта Figure

        #отделяем часть графика x с границами N1,N2
        x_tek=[]#отделили глубины на отрезке x 
        x_tek_val=[]#отделили значения на отрезке x
        for i in range(N1,N2+1):
            x_tek.append(x_interval[i])
            x_tek_val.append(x_interp[i])


        y_tek=[]#отделили глубины на отрезке y
        y_tek_val=[]#отделили значения на отрезке y

        koef_kor=[]#список для хранения границ корреляции

        #перебираем график y учитывая отклонение M
        for j in range(N2-N1-M,N2-N1+M+1):#перебираем возможные размеры окна
            for k in range(min(len(y_interval),len(y_interp))-j):#перебираем первую границу окна от 0 до конца графика
                        y_tek=[]#отделили глубины на отрезке y
                        y_tek_val=[]#отделили значения на отрезке y
                        for i in range(k,k+j):
                                y_tek.append(y_interval[i])
                                y_tek_val.append(y_interp[i])
                
                        #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
                        if len(x_tek_val) != len(y_tek_val):
                            c1=np.linspace(min(min(x_tek),min(y_tek)),max(max(x_tek),max(y_tek)), max(len(x_tek),len(y_tek)))
                            x_tek_interp=np.interp(c1,x_tek,x_tek_val)
                            y_tek_interp=np.interp(c1,y_tek,y_tek_val)
                        else:
                            x_tek_interp=x_tek_val
                            y_tek_interp=y_tek_val
                        miny0=float('inf')
                        miny1=float('inf')
                        ytek=[y_tek[0],y_tek[-1]]
                        for i in y_dict:
                                if miny0>abs(i-y_tek[0]):
                                        ytek[0]=y_dict[i]
                                        miny0=abs(i-y_tek[0])
                                if miny1>abs(i-y_tek[-1]):
                                        ytek[1]=y_dict[i]
                                        miny1=abs(i-y_tek[-1])
        ##                                print(ytek)
                        if ytek[0]>=distance[0] and ytek[-1]<=distance[-1]:
                                #запишем коэффициенты корреляции для каждой получившейся пары окон
                                #0 и 1 элементы это границы окна y
                                #2 элемент это сам коэффициент
                                koef_kor.append([k,k+j,pearsonr(x_tek_interp, y_tek_interp)[0]])
                        

        #после заполнения всех возможных коэффициентов корреляции найдем максимальный
        if len(koef_kor)==0:
            print('Нет пути')
        else:
                max_koef=float('-inf')
                ind=0
                vse=0
                for i in koef_kor:
                    if i[2]>max_koef:
                        max_koef=i[2]
                        ind=vse
                    vse+=1
##                print('Итог:',y[koef_kor[ind][0]],'\t',y[koef_kor[ind][1]],max_koef)
                return y[koef_kor[ind][0]],y[koef_kor[ind][1]]


        ##                i=N1#для графика x
        ##                for j in range(koef_kor[ind][0],koef_kor[ind][1]+1,10):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
        ##                                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='green')
        ##                                i+=10
        ####                                print((x_val[i],y_val[j]),(x[i],y[j]))
        ##                   
        ##                plt.show()
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

def dtw_all():

        f1=input('Введите номер скважины ')
        f2=input('Введите номер скважины ')
        values1 = [] # считываем значения из первого файла
        v1=[]
        v2=[]
        values2 = [] # считываем значения из второго файла
        read(v1,values1,f1+".txt")
        read(v2,values2,f2+".txt")
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
            fig = plt.figure()   # Создание объекта Figure
            plt.plot(values1,v1)
            plt.plot(values2,v2, color="red")

            i=0
                    
            for j in range(0,len(result_x),10):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
                plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet')
            plt.show()
        else:
            messagebox.showinfo("GUI Python", 'Путь не найден')
def dtw_interval(f1,f2,a1=0,a2=0):
        values1 = [] # считываем значения из первого файла
        v1=[]
        v2=[]
        values2 = [] # считываем значения из второго файла
        read(v1,values1,'s'+f1+".txt")
        read(v2,values2,'s'+f2+".txt")
##        if f1=='97':
##            v1=np.linspace(min(v1)-5,max(v1)+5,len(v1))
##        elif f2=='97':
##            v2=np.linspace(min(v2)-5,max(v2)+5,len(v2))
        way = dtw(values1, len(values1), values2, len(values2))
        result_x=[]
        result_y=[]
        if way is not None:
            # выводим путь
##            print("Way:")
            with open("result.txt", "w") as f:
                for k in way:
                    i = k // len(values2)
                    j = k % len(values2)

##                    print(i + 1, j + 1)
                    f.write(str(i + 1) + " " + str(j + 1) + "\n")
           
            read(result_x,result_y,"result.txt")

            plt.plot(values1,v1)
            plt.plot(values2,v2, color="red")
            if float(message9.get().replace(',','.'))<0 or message9.get()=='':
                messagebox.showinfo("GUI Python", 'Неверная левая граница')
            else:
                if float(message8.get().replace(',','.'))<0 or message8.get()=='':
                    messagebox.showinfo("GUI Python", 'Неверная правая граница')
                else:
##                    N1=float(message8.get())
##                    N2=float(message9.get())
                    a=a1
                    b=a2
                    N1x=a
                    mina=float('inf')
                    minb=float('inf')
                    a_new=0
                    b_new=0
                    for i in range(len(v1)):
                        if v1[i]==a:
                            a_new=i
                        elif mina>abs(v1[i]-a):
                            mina=abs(v1[i]-a)
                            a_new=i
                        if v1[i]==b:
                            b_new=i
                        elif minb>abs(v1[i]-b):
                            minb=abs(v1[i]-b)
                            b_new=i
                    a=a_new
                    b=b_new
##                    print('маркеры:',v1[a],v1[b])
                    distance=angle(v1[a],v1[b],f1,f2)
                    i=0
                    N1y=v1[a]
                    fig = plt.figure()   # Создание объекта Figure
##                    plt.plot(values1,v1)
##                    plt.plot(values2,v2, color="red")
                    f=True
                    itog=[]
                    for j in range(0,len(result_x),1):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
                        if a<=result_x[j]<=b:
                            itog.append(v2[int(result_y[j])-1])
                            if f:
                                    N2x=values2[int(result_y[j])-1]
                                    N2y=v2[int(result_y[j])-1]
                                    f=False
                            else:
                                    N3y=v2[int(result_y[j])-1]
##                            plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet')
##                            print((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]))
##                    plt.show()
                    
                    if itog[0]>=distance[0] and itog[-1]<=distance[-1]:
##                        print("Итог:",itog[0],'\t',itog[-1])
                        return itog[0],itog[-1]
                    else:
                        print('нет пути')
        else:
            messagebox.showinfo("GUI Python", 'Путь не найден')
def all():
    fig = plt.figure()   # Создание объекта Figure
    #1  
    x=list()#глубины
    x_val=list()#значения
    read(x,x_val,"x.txt")
    x_dict={}#хранится соответствие глубин с интервалом [0,1]
    x_interval=list()#хранятся новые глубины

    #2 
    y=list()#глубины
    y_val=list()#значения
    read(y,y_val,"y.txt")
    y_dict={}#хранится соответствие глубин с интервалом [0,1]
    y_interval=list()#хранятся новые глубины

    #поднимем один график для удобства
    for i in range(len(x_val)):
        x_val[i]+=2
        
    for i in range(len(x)):
        x_dict[i*1/len(x)]=x[i]
        #изменяем глубины на интервал [0,1]
        x_interval.append(i*1/len(x))


    for i in range(len(y)):
        y_dict[i*1/len(y)]=y[i]
        #изменяем глубины на интервал [0,1]
        y_interval.append(i*1/len(y))

    #переинтерполируем на новом интервале [0,1] оба графика
    c=np.linspace(min(min(x_interval),min(y_interval)),max(max(x_interval),max(y_interval)), (len(x_interval)+len(y_interval))//2)
    x_interp=np.interp(c,x_interval,x_val)#новое значение x
    y_interp=np.interp(c,y_interval,y_val)#новое значение y

    x_interp_txt=open( "x_interp.txt", 'w' )
    y_interp_txt=open( "y_interp.txt", 'w' )

    write(x_interp,x_interp_txt)
    write(y_interp,y_interp_txt)

    #вводим границы окна и отклонение
    #N1,N2=[int(i) for i in input("Введите границы окна:").split()]
   
    if message.get()=='':
        messagebox.showinfo("GUI Python", 'Введите левую границу')
    else:
        if message2.get()=='':
            messagebox.showinfo("GUI Python", 'Введите правую границу')
        else:
            if message3.get()=='':
                messagebox.showinfo("GUI Python", 'Введите отклонение')
            else:

                print (fig.axes)   # Список текущих областей рисования пуст
                print (type(fig))   # тип объекта Figure


                # После нанесения графического элемента в виде маркера
                # список текущих областей состоит из одной области
                print (fig.axes)
                N1=int(message.get())
                N2=int(message2.get())
                M=int(message3.get())
                #отделяем часть графика x с границами N1,N2
                x_tek=[]#отделили глубины на отрезке x 
                x_tek_val=[]#отделили значения на отрезке x
                for i in range(N1,N2+1):
                    x_tek.append(x_interval[i])
                    x_tek_val.append(x_interp[i])


                y_tek=[]#отделили глубины на отрезке y
                y_tek_val=[]#отделили значения на отрезке y

                koef_kor=[]#список для хранения границ корреляции

                #перебираем график y учитывая отклонение M
                for j in range(N2-N1-M,N2-N1+M+1):#перебираем возможные размеры окна
                    for k in range(len(y)-(N2-N1+M)):#перебираем первую границу окна от 0 до конца графика
                                for i in range(k,k+j+1):
                                        y_tek.append(y_interval[i])
                                        y_tek_val.append(y_interp[i])
                        
                                #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
                                if len(x_tek_val) != len(y_tek_val):
                                    c1=np.linspace(min(min(x_tek),min(y_tek)),max(max(x_tek),max(y_tek)), (len(x_tek)+len(y_tek))//2)
                                    x_tek_interp=np.interp(c1,x_tek,x_tek_val)
                                    y_tek_interp=np.interp(c1,y_tek,y_tek_val)
                                else:
                                    x_tek_interp=x_tek_val
                                    y_tek_interp=y_tek_val  
                                #запишем коэффициенты корреляции для каждой получившейся пары окон
                                #0 и 1 элементы это границы окна y
                                #2 элемент это сам коэффициент
                                koef_kor.append([k,k+j,pearsonr(x_tek_interp, y_tek_interp)[0]])
                                

                #после заполнения всех возможных коэффициентов корреляции найдем максимальный

                max_koef=float('-inf')
                ind=0
                vse=0
                for i in koef_kor:
                    if i[2]>max_koef:
                        max_koef=i[2]
                        ind=vse
                    vse+=1
                print(koef_kor[ind][0],koef_kor[ind][1],max_koef)

                        
                plt.plot(x_val,x)
                plt.plot(y_val,y, color="red")

                i=N1#для графика x
                for j in range(koef_kor[ind][0],koef_kor[ind][1]+1,10):#начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
                                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='green')
                                i+=10
        values1 = [] # считываем значения из первого файла
        v1=[]
        v2=[]
        values2 = [] # считываем значения из второго файла
        read(v1,values1,"x.txt")
        read(v2,values2,"y.txt")
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
            if int(message9.get())<0 or message9.get()=='':
                messagebox.showinfo("GUI Python", 'Неверная левая граница')
            else:
                if int(message8.get())<0 or message8.get()=='':
                    messagebox.showinfo("GUI Python", 'Неверная правая граница')
                else:
                    N1=int(message8.get())
                    N2=int(message9.get())
                    
                    i=0
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

#создаем поля ввода 
#левая граница
message = StringVar()

kor_entry = Entry(textvariable=message,width=50)
kor_entry.grid(row=0,column=1, padx=5, pady=5)
kor_label = Label(text="Введите левую границу интервала:",width=50)
kor_label.grid(row=0, column=0, sticky="w")

#правая граница
message2 = StringVar()

kor_entry2 = Entry(textvariable=message2,width=50)
kor_entry2.grid(row=1,column=1, padx=5, pady=5)
kor_label2 = Label(text="Введите правую границу интервала:",width=50)
kor_label2.grid(row=1, column=0, sticky="w")

#отклонение
message3 = StringVar()

kor_entry3 = Entry(textvariable=message3,width=50)
kor_entry3.grid(row=2,column=1, padx=5, pady=5)
kor_label3 = Label(text="Введите отклонение:",width=50)
kor_label3.grid(row=2, column=0, sticky="w")

#кнопка корреляции
btn1=Button(tk, text='Построить соответсвие методом корреляции',width=50,command=perebor)
btn1.grid(row=3,column=1, padx=5, pady=5, sticky="e")

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

btn3=Button(tk, text='Построить соответсвие алгоритмом DTW на заданом интервале',width=50,command=perebor)
btn3.grid(row=11,column=1, padx=5, pady=5, sticky="e")

btn4=Button(tk, text='Построить DTW и корреляцию на интервале',width=50,command=all)
btn4.grid(row=12,column=1, padx=5, pady=5, sticky="e")

btn5=Button(tk, text='Построить кривые',width=50,command=draw)
btn5.grid(row=13,column=1, padx=5, pady=5, sticky="e")
