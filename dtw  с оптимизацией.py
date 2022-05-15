from tkinter import *
import numpy as np
from tkinter import ttk
from math import *
import random
import math
from math import sqrt
from scipy.stats.stats import pearsonr
import pickle
from tkinter import messagebox

import matplotlib as mpl
import matplotlib.pyplot as plt

boltsman = 'boltsman'
koshi = 'koshi'

temperature_mode = boltsman # koshi

# функция перехода
def P(e_old, e_new, T):
    return math.exp((e_old - e_new) / T)


# получение температуры
def get_tempetature(T0, iteration):
    if combo_opt.get()=='Коши':
        temperature_mode = koshi
    else:
        temperature_mode = boltsman
    if temperature_mode == boltsman:
        return T0 / math.log(1 + iteration)

    return T0 / iteration

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
            
def perebor():
    s=[['97','96','87'],['96','97','87'],['97','87','96'],['87','96','97'],['87','97','96'],['96','87','97']]
    markers={'97':[2982.6-5,2993.1+5],'96':[3012.4,3020.4],'87':[3076.8,3087]}
    for i in s:
        print(i)
        k1,k2=dtw_interval(i[0],i[1],a1=markers[i[0]][0],a2=markers[i[0]][1],a3=markers[i[1]][0],a4=markers[i[1]][0])
        print(k1,'\t',k2)
        k1,k2=dtw_interval(i[1],i[2],a1=k1,a2=k2)
        print(k1,'\t',k2)
        k1,k2=dtw_interval(i[2],i[0],a1=k1,a2=k2)
        print(k1,'\t',k2)
        
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
##        z96+=100
        
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
        
##        #падение на 20м
##        if f1=='96':
##                Z=[i+100 for i in Z]
##        if f2=='96':
##                Z=[i+100 for i in Z]
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
    plt.plot(y_val,y, color="red")
    plt.show()


def dtw(s, n, h, m,firstLineVariant,deflateVariant,stretchVariant,lastLineVariant,deflateforfeit,stretchforfeit):
    
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
##                    #Привязка первой точки образа
##                        #1-Привязывать обязательно с первой точки исходной кривой
##                        #2-Разрешено привязывать с любой точки исходной кривой
##                    firstLineVariant = int(message4.get())
##                    
##                    #Сжатие образца
##                        #1-сжатие запрещено
##                        #2-сжатие разрешено без штрафа
##                        #3-сжатие разрешено со штрафом
##                    deflateVariant = int(message5.get())
##                    
##                    #растяжение образца
##                        #1-растяжение запрещено
##                        #2-растяжение разрешено без штрафа
##                        #3-растяжение разрешено со штрафом
##                    stretchVariant = int(message6.get())
##                    
##                    #Привязка последней точки образа
##                        #1-разрешено заканчиваться на любой точке исходной кривой
##                        #2-привязывать обязательно к последней точке исходной кривой
##                    lastLineVariant = int(message7.get())

                    #величина штрафа за сжатие
##                    deflateforfeit=int(message10.get())
##
##                    #величина штрафа за растяжение
##                    stretchforfeit=int(message11.get())
                    
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
                                D[i + 1][j] = min(D[i + 1][j], D[i][j] + deflateforfeit*abs(s[i + 1]- h[j])) # сжатие разрешено со штрафом
                                ways[i + 1][j] = ways[i + 1][j] if D[i + 1][j] < D[i][j] + deflateforfeit*abs(s[i + 1] - h[j]) else UP

                            # растяжение
                            if stretchVariant == 1:
                                D[i][j + 1] = D[i][j + 1] # растяжение запрещено
                                ways[i][j + 1] = ways[i][j + 1]
                            elif stretchVariant == 1:
                                D[i][j + 1] = min(D[i][j + 1], D[i][j]) # растяжение разрешено без штрафа
                                ways[i][j + 1] = ways[i][j + 1] if D[i][j + 1] < D[i][j] else LEFT
                            elif stretchVariant == 3:
                                D[i][j + 1] = min(D[i][j + 1], D[i][j] + stretchforfeit*abs(s[i] - h[j + 1])) # растяжение разрешено со штрафом
                                ways[i][j + 1] = ways[i][j + 1] if D[i][j + 1] < D[i][j] + stretchforfeit*abs(s[i] - h[j + 1]) else LEFT

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

def dtw_interval(f1,f2,a1=0,a2=0,a3=0,a4=0):
        values1 = [] # считываем значения из первого файла
        v1=[]
        v2=[]
        values2 = [] # считываем значения из второго файла
        read(v1,values1,"s"+f1+".txt")
        read(v2,values2,"s"+f2+".txt")
        if f1=='97':
            v1=np.linspace(min(v1)-5,max(v1)+5,len(v1))
        elif f2=='97':
            v2=np.linspace(min(v2)-5,max(v2)+5,len(v2))
        intervals=[]
        intervals_copy=[]
        
        deflateforfeit=int(message10.get())
        stretchforfeit=int(message11.get())
        N1=a1
        N2=a2
        N3=a3
        N4=a4
        minN1=float('inf')
        minN2=float('inf')
        N1_new=0
        N2_new=0
        for i in range(len(v1)):
            if v1[i]==N1:
                N1_new=i
            elif minN1>abs(v1[i]-N1):
                minN1=abs(v1[i]-N1)
                N1_new=i
            if v1[i]==N2:
                N2_new=i
            elif minN2>abs(v1[i]-N2):
                minN2=abs(v1[i]-N2)
                N2_new=i
        N1=N1_new
        N2=N2_new
        distance=angle(v1[N1],v1[N2],f1,f2)
        minN3=float('inf')
        minN4=float('inf')
        N1_new=0
        N2_new=0
        for i in range(len(v2)):
            if v2[i]==N3:
                N3_new=i
            elif minN3>abs(v2[i]-N3):
                minN3=abs(v2[i]-N3)
                N3_new=i
            if v2[i]==N4:
                N4_new=i
            elif minN4>abs(v2[i]-N4):
                minN4=abs(v2[i]-N4)
                N4_new=i
        N3=N3_new
        N4=N4_new
        for i in range(len(v2)):
            if v2[i]==N3:
                N3=i
            if v2[i]==N4:
                N4=i    
##        print(v1[N1],v1[N2],v2[N3],v2[N4])
        way = dtw(values1, len(values1), values2, len(values2),1,1,1,1,int(message10.get()),int(message11.get()))
        result_x=[]
        result_y=[]

        if way is not None:
            # выводим путь
##                            print("Way:")
            with open("result.txt", "w") as f:
                for k in way:
                    i = k // len(values2)
                    j = k % len(values2)

##                                    print(i + 1, j + 1)
                    f.write(str(i + 1) + " " + str(j + 1) + "\n")
            read(result_x,result_y,"result.txt")
            for j in range(0,len(result_y)):
                    if int(result_x[j])-1==N1:
                        d=v2[int(result_y[j])-1]
                    if int(result_x[j])-1==N2:
                        d0=v2[int(result_y[j])-1]           
            d1=d-v2[N3]                    
            d2=d0-v2[N4]
            if d>=distance[0] and d0<=distance[-1]:
                intervals.append([d,d0,abs(d1)+abs(d2),1,1,1,1,int(message10.get()),int(message11.get())])
                intervals_copy.append([result_x,result_y,abs(d1)+abs(d2),1,1,1,1,int(message10.get()),int(message11.get())])

        for q in range(2):
            for w in range(3):
                for o in range(3):
                    for h in range(2):
                        way = dtw(values1, len(values1), values2, len(values2),q+1,w+1,o+1,h+1,int(message10.get()),int(message11.get()))
                        result_x=[]
                        result_y=[]

                        if way is not None:
                            # выводим путь
##                            print("Way:")
                            with open("result.txt", "w") as f:
                                for k in way:
                                    i = k // len(values2)
                                    j = k % len(values2)

##                                    print(i + 1, j + 1)
                                    f.write(str(i + 1) + " " + str(j + 1) + "\n")
                            read(result_x,result_y,"result.txt")
                            for j in range(0,len(result_y)):
                                    if int(result_x[j])-1==N1:
                                        d=v2[int(result_y[j])-1]
                                    if int(result_x[j])-1==N2:
                                        d0=v2[int(result_y[j])-1]           
                            d1=d-v2[N3]                    
                            d2=d0-v2[N4]
                            if d>=distance[0] and d0<=distance[-1]:
                                intervals.append([d,d0,abs(d1)+abs(d2),q+1,w+1,o+1,h+1,int(message10.get()),int(message11.get())])
                                intervals_copy.append([result_x,result_y,abs(d1)+abs(d2),q+1,w+1,o+1,h+1,int(message10.get()),int(message11.get())])
##                            print(q+1,w+1,o+1,h+1,abs(d1)+abs(d2))
##                        else:
##                            print(q+1,w+1,o+1,h+1,'No way')


        
        
        for i in intervals_copy:
            deflateforfeit=int(message10.get())
            stretchforfeit=int(message11.get())
            T = 1
##                        print(i[3],i[4],i[5],i[6])
            if i[-5]==3 or i[-4]==3:
                    for iter in range(1,int(message7_opt.get())+1):
                            interval_loc=[]
                            
                            if i[-5]==3 and i[-4]==3:
                                stretchforfeit=random.choice(np.arange(float(message3_opt.get()),float(message4_opt.get()),float(message5_opt.get())))
                                deflateforfeit = random.choice(np.arange(float(message0_opt.get()),float(message1_opt.get()),float(message2_opt.get())))
                            elif i[-4]==3 :
                                stretchforfeit=random.choice(np.arange(float(message3_opt.get()),float(message4_opt.get()),float(message5_opt.get())))
                            elif i[-5]==3:
                                deflateforfeit = random.choice(np.arange(float(message0_opt.get()),float(message1_opt.get()),float(message2_opt.get())))
                                
                            way = dtw(values1, len(values1), values2, len(values2),i[3],i[4],i[5],i[6],deflateforfeit,stretchforfeit)
                            result_x=[]
                            result_y=[]
                            if way is not None:
                                # выводим путь
                            ##                            print("Way:")
                                with open("result.txt", "w") as f:
                                    for k in way:
                                        o = k // len(values2)
                                        j = k % len(values2)

                            ##                                    print(i + 1, j + 1)
                                        f.write(str(o + 1) + " " + str(j + 1) + "\n")
                                read(result_x,result_y,"result.txt")
                                
                                for j in range(0,len(result_y)):
                                    if int(result_x[j])==N1:
                                        d=v2[int(result_y[j])-1]
                                    if int(result_x[j])==N2:
                                        d0=v2[int(result_y[j])-1]        
                                d1=d-v2[N3]                    
                                d2=d0-v2[N4]
##                                print(v2[int(result_y[0])],v2[int(result_y[-1])-1])
                                
                                e_old, e_new = i[2],abs(d1)+abs(d2)
##                                    print(abs(d1)+abs(d2))
                                T = get_tempetature(T, (iter + 1) / iter)
                                if e_new<e_old:
                                        interval_loc.append([d,d0,e_new,i[3],i[4],i[5],i[6],deflateforfeit,stretchforfeit])
##                                        print([e_new,i[3],i[4],i[5],i[6],deflateforfeit,stretchforfeit])
                                else:
                                        if P(e_old, e_new, T) >= random.random():
                                                interval_loc.append([d,d0,e_new,i[3],i[4],i[5],i[6],deflateforfeit,stretchforfeit])
##                                                print([e_new,i[3],i[4],i[5],i[6],deflateforfeit,stretchforfeit])
                                if e_new==0 or T<=0:
                                    break

                    if interval_loc!=[]:
                            min_discrepancy=float('inf') 
                            index=0
                            val=0
                            for z in interval_loc:
                                if z!=[]:
                                    if z[2]<min_discrepancy:
                                        min_discrepancy=z[2]
                                        index=val
                                    val+=1
##                            if interval_loc[index][0]>=distance[0] and interval_loc[index][1]<=distance[-1]:
                            intervals.append(interval_loc[index])
##                            print(interval_loc[index][0],interval_loc[index][1])

        
        
        if intervals==[]:
            print('Нет пути')
        else:
            min_discrepancy=intervals[0][2]
            index=0
            val=0
##            print('final')
            for i in intervals:
##                print(i[2:])
##                print(v2[int(i[1][0])-1],v2[int(i[1][-1])-1])
                if i[2]<min_discrepancy and intervals[val][0]!=intervals[val][1]:
                    min_discrepancy=i[2]
                    index=val
                val+=1
            
##            result_x=intervals[index][0]
##            result_y=intervals[index][1]
##            print('final:',intervals[index][2:])
##            print('Итог',intervals[index][0],'\t',intervals[index][1])
            return intervals[index][0],intervals[index][1]

        
        
        #поднимем один график для удобства
        for a in range(len(values1)):
            values1[a]+=2
            
        i=0
        fig = plt.figure()   # Создание объекта Figure
        #строим заданный пользователем интервал
        i=N1#для графика x
        for j in range(N3,N4+1,10):
##                        plt.plot((values1[i],values2[j]),(v1[i],v2[j]),color='black',lw=0.5)
                        i+=10
        plt.plot((values1[N1],values2[N3]),(v1[N1],v2[N3]),color='lightblue',lw=2)
        plt.plot((values1[N2],values2[N4]),(v1[N2],v2[N4]),color='lightblue',lw=2, label="желаемый интервал")
                
##        plt.plot((values1[N1],values2[N2]),(v1[N1],v2[N2]),color='lightblue',lw=0.5)
##        plt.plot((values1[N3],values2[N4]),(v1[N3],v2[N4]),color='lightblue',lw=0.5, label="Интервал, который ввел пользователь")
    
        plt.plot(values1,v1)
        plt.plot(values2,v2, color="red")
##        for j in range(0,len(result_x),10):
##            if N1==result_x[j] and N2==result_x[j]:
##                plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet',label='Итог')

##        for j in range(0,len(result_y)):
##            if int(result_x[j])-1==N1:
##                plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet',lw=2)
####                print((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]))
##            if int(result_x[j])-1==N2:
##                plt.plot((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]),color='violet',label='Итог',lw=2)
##    ##        plt.plot((values1[N2],values2[int(result_y[-1])-1]),(v1[N2],v2[int(result_y[-1])-1]),color='violet',label='Итог')
####                print((values1[int(result_x[j])-1],values2[int(result_y[j])-1]),(v1[int(result_x[j])-1],v2[int(result_y[j])-1]))
##        plt.legend()
####        plt.show()


NONE = 1
LEFT = 2
UP = 4
INFINITY = 1e300 # беконечность

#создаем окно для кнопок 
tk=Tk()
tk.title("Параметры алгоритма DTW")

tk.geometry('1200x500')
tk.resizable(height = 0, width = 0)
 

#левая граница
message4 = StringVar()

dtw_entry0 = Entry(tk,textvariable=message4,width=50)
dtw_entry0.grid(row=0,column=1, padx=5, pady=5)
dtw_label = Label(tk,text="Введите привязку первой точки образа  "+"\n"+"1-Привязывать обязательно с первой точки исходной кривой "+"\n"+" 2-Разрешено привязывать с любой точки исходной кривой",width=50)
dtw_label.grid(row=0, column=0, sticky="w")

message5 = StringVar()

dtw_entry1 = Entry(tk,textvariable=message5,width=50)
dtw_entry1.grid(row=1,column=1, padx=5, pady=5)
dtw_label = Label(tk,text="Введите cжатие образца"+"\n"+"1-сжатие запрещено "+"\n"+"2-сжатие разрешено без штрафа"+"\n"+" 3-сжатие разрешено со штрафом",width=50)
dtw_label.grid(row=1, column=0, sticky="w")

message10 = StringVar()
dtw_label10=Label(tk,text='Введите штраф за сжатие')
dtw_label10.grid(row=9,column=0, padx=5, pady=5)
dtw_entry10=Entry(tk,textvariable=message10,width=10)
dtw_entry10.grid(row=9,column=1,sticky='w', padx=30, pady=5)

message6 = StringVar()
dtw_entry2 = Entry(tk,textvariable=message6,width=50)
dtw_entry2.grid(row=3,column=1, padx=5, pady=5)
dtw_label = Label(tk,text="Введите растяжение образца"+"\n"+" 1-растяжение запрещено "+"\n"+"2-растяжение разрешено без штрафа"+"\n"+" 3-растяжение разрешено со штрафом",width=50)
dtw_label.grid(row=3, column=0, sticky="w")

message11 = StringVar()
dtw_label11=Label(tk,text='Введите штраф за растяжение')
dtw_label11.grid(row=10,column=0)
dtw_entry11=Entry(tk,textvariable=message11,width=10)
dtw_entry11.grid(row=10,column=1,sticky='w', padx=30, pady=5)

message7 = StringVar()
dtw_entry3 = Entry(tk,textvariable=message7,width=50)
dtw_entry3.grid(row=4,column=1, padx=5, pady=5)
dtw_label = Label(tk,text="Введите привязку последней точки образа "+"\n"+"1-разрешено заканчиваться на любой точке исходной кривой"+"\n"+" 2-привязывать обязательно к последней точке исходной кривой",width=50)
dtw_label.grid(row=4, column=0, sticky="w")

#левая граница
message8 = StringVar()

dtw_int_entry = Entry(tk,textvariable=message8,width=50)
dtw_int_entry.grid(row=5,column=1, padx=5, pady=5)
dtw_int_label = Label(tk,text="Введите левую границу интервала первого графика:",width=50)
dtw_int_label.grid(row=5, column=0, sticky="w")

#правая граница
message9 = StringVar()

dtw_int_entry4 = Entry(tk,textvariable=message9,width=50)
dtw_int_entry4.grid(row=6,column=1, padx=5, pady=5)
dtw_int_label4 = Label(tk,text="Введите правую границу интервала первого графика:",width=50)
dtw_int_label4.grid(row=6, column=0, sticky="w")

#левая граница
message12 = StringVar()

dtw_int_entry = Entry(tk,textvariable=message12,width=50)
dtw_int_entry.grid(row=7,column=1, padx=5, pady=5)
dtw_int_label = Label(tk,text="Введите левую границу интервала второго графика:",width=50)
dtw_int_label.grid(row=7, column=0, sticky="w")

#правая граница
message13 = StringVar()

dtw_int_entry4 = Entry(tk,textvariable=message13,width=50)
dtw_int_entry4.grid(row=8,column=1, padx=5, pady=5)
dtw_int_label4 = Label(tk,text="Введите правую границу интервала второго графика:",width=50)
dtw_int_label4.grid(row=8, column=0, sticky="w")

btn3=Button(tk,text='Построить соответсвие алгоритмом DTW на заданом интервале',width=50,command=perebor)
btn3.grid(row=11,column=1, padx=5, pady=5, sticky="e")

btn5=Button(tk,text='Построить кривые',width=50,command=draw)
btn5.grid(row=12,column=1, padx=5, pady=5, sticky="e")

###создание второго окна для оптимизации
##tk=Tk()
##tk.title("Параметры оптимизации")
##
##tk.geometry('400x250')
##tk.resizable(height = 0, width = 0)

#минимальный штраф за сжатие
message0_opt = StringVar()

opt_entry0 = Entry(tk,textvariable=message0_opt,width=20)
opt_entry0.grid(row=0,column=3, padx=5, pady=5)
opt_label0 = Label(tk,text="Минимальный штраф за сжатие")
opt_label0.grid(row=0, column=2, sticky="w")

#максимальный штраф за сжатие
message1_opt = StringVar()

opt_entry1 = Entry(tk,textvariable=message1_opt,width=20)
opt_entry1.grid(row=1,column=3, padx=5, pady=5)
opt_label1 = Label(tk,text="Максимальный штраф за сжатие")
opt_label1.grid(row=1, column=2, sticky="w")

#шаг- сжатие
message2_opt = StringVar()

opt_entry2 = Entry(tk,textvariable=message2_opt,width=20)
opt_entry2.grid(row=2,column=3, padx=5, pady=5)
opt_label2 = Label(tk,text="Шаг-сжатие")
opt_label2.grid(row=2, column=2, sticky="w")

#минимальный штраф за растяжение
message3_opt = StringVar()

opt_entry3 = Entry(tk,textvariable=message3_opt,width=20)
opt_entry3.grid(row=3,column=3, padx=5, pady=5)
opt_label3 = Label(tk,text="Минимальный штраф за растяжение")
opt_label3.grid(row=3, column=2, sticky="w")

#максимальный штраф за сжатие
message4_opt = StringVar()

opt_entry4 = Entry(tk,textvariable=message4_opt,width=20)
opt_entry4.grid(row=4,column=3, padx=5, pady=5)
opt_label4 = Label(tk,text="Максимальный штраф за растяжение")
opt_label4.grid(row=4, column=2, sticky="w")

#шаг- сжатие
message5_opt = StringVar()

opt_entry5 = Entry(tk,textvariable=message5_opt,width=20)
opt_entry5.grid(row=5,column=3, padx=5, pady=5)
opt_label5 = Label(tk,text="Шаг-растяжение")
opt_label5.grid(row=5, column=2, sticky="w")

#варианты изменения температуры
combo_opt = ttk.Combobox(tk, values=['Коши','Больцман'],width=17)
combo_opt.grid(row=6, column=3)
opt_label6 = Label(tk,text="Изменение температуры")
opt_label6.grid(row=6, column=2, sticky="w")

#количество итераций
message7_opt = StringVar()

opt_entry7 = Entry(tk,textvariable=message7_opt,width=20)
opt_entry7.grid(row=7,column=3, padx=5, pady=5)
opt_label7 = Label(tk,text="Количество итераций")
opt_label7.grid(row=7, column=2, sticky="w")


