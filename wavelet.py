from tkinter import *
import numpy as np
import random
from math import *
from scipy.stats.stats import pearsonr
import pickle
from tkinter import messagebox
from scipy.fft import fft, ifft
import pywt

import matplotlib as mpl
import matplotlib.pyplot as plt

#Функция записи в файл
def write(lst,nametxt):
        for item in lst:
            nametxt.write("%s\n" % item)
#Функция чтения из файла
def read(lst,lst_val,nametxt):
        with open(nametxt) as file:
                for line in file.readlines():
                        a,b=[float(i) for i in line.split()]
                        lst.append(a)
                        lst_val.append(b)


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
##        z96+=20
        
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
        
        #падение на 20м
##        if f1=='87':
##                Z=[i+20 for i in Z]

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
                   
        print('маркеры MD',N1MD,N2MD)
        N1y=Z[indN1]
        N2y=Z[indN2]
        print('маркеры MD в Z',N1y,N2y)
        
        #сдвиг
        N1y-=c
        N2y+=c
        print('Z после сдвига',N1y,N2y)
        
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
        print('Значения Z после сдвига на второй скважине',N1Z,N2Z)
        N1y=MD2[indN1]
        N2y=MD2[indN2]
        
        print('Допустимый:',N1y,N2y)
        return N1y,N2y

def _functional1(supp_coeffs, target_coeffs):
    
        integral = 0
        ca1 = supp_coeffs[0]
        ca2 = target_coeffs[0]

        integral += sum(pow((ca1 - ca2), 2))
        for i in range(1, len(supp_coeffs) ):
            cd1 = supp_coeffs[i]['d']
            cd2 = target_coeffs[i]['d']

            for j in range(0, 6):
                for k in range(0, len(ca1)):
                    integral += (cd1[k] - cd2[k]) ** 2

        return integral
    
def fur():
    #1
    f1=input('Введите номер скважины ')
    f2=input('Введите номер скважины ')
    x=list()#глубины
    x_val=list()#значения
    read(x,x_val,f1+".txt")
##    c=np.linspace(0,len(x),128)
##    x=np.interp(c,[i for i in range(0,len(x))],x)
##    x_val=np.interp(c,[i for i in range(0,len(x_val))],x_val)

    #2 
    y=list()#глубины
    y_val=list()#значения
    read(y,y_val,f2+".txt")
##    c=np.linspace(0,len(y),128)
##    y=np.interp(c,[i for i in range(0,len(y))],y)
##    y_val=np.interp(c,[i for i in range(0,len(y_val))],y_val)

        
    N1=float(message.get().replace(',','.'))
    N2=float(message2.get().replace(',','.'))
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
    distance=angle(x[N1],x[N2],f1,f2)
    #отделяем часть графика x с границами N1,N2
    x_tek=[]#отделили глубины на отрезке x 
    x_tek_val=[]#отделили значения на отрезке x

    for i in range(N1,N2+1):
        x_tek.append(x[i])
        x_tek_val.append(x_val[i])

    y_tek=[]#отделили глубины на отрезке y
    y_tek_val=[]#отделили значения на отрезке y

    pog=[]

    #перебираем график y учитывая отклонение M
    for j in range(N2-N1-M,N2-N1+M+1):#перебираем возможные размеры окна
        for k in range(len(y_val)-j):#перебираем первую границу окна от 0 до конца графика
                    y_tek=[]#отделили глубины на отрезке y
                    y_tek_val=[]#отделили значения на отрезке y
                    for i in range(k,k+j+1):
                            y_tek.append(y[i])
                            y_tek_val.append(y_val[i])
            
                    #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
                    if len(x_tek_val) != len(y_tek_val):
                        c1=np.linspace(min(min(x_tek),min(y_tek)),max(max(x_tek),max(y_tek)), max(len(x_tek),len(y_tek)))
                        x_tek_interp=np.interp(c1,x_tek,x_tek_val)
                        y_tek_interp=np.interp(c1,y_tek,y_tek_val)
                    else:
                        x_tek_interp=x_tek_val
                        y_tek_interp=y_tek_val
                
                    #нормировка
                    x_tek_interp=(x_tek_interp-np.min(x_tek_interp))/(np.max(x_tek_interp)-np.min(x_tek_interp))
                    y_tek_interp=(y_tek_interp-np.min(y_tek_interp))/(np.max(y_tek_interp)-np.min(y_tek_interp))
                    #вейвлет
                    x_tek_interp=pywt.wavedecn(x_tek_interp, 'haar', level=6)
                    y_tek_interp=pywt.wavedecn(y_tek_interp, 'haar', level=6)
                    pogr_tek= _functional1(x_tek_interp, y_tek_interp)
                    pog.append([y[k],y[k+j],pogr_tek])
    if len(pog)==0:
            print('Нет пути')
    else:
            minpog=float('inf')
            ind=0
            vse=0
            for i in pog:
                if i[2]<minpog:
                    minpog=i[2]
                    ind=vse
                vse+=1
            print('Итог:',pog[ind])
    
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
btn1=Button(tk, text='Построить соответсвие методом корреляции',width=50,command=fur)
btn1.grid(row=3,column=1, padx=5, pady=5, sticky="e")                
