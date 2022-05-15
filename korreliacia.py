from tkinter import *
import numpy as np
import random
from math import sqrt
from scipy.stats.stats import pearsonr
import pickle
from tkinter import messagebox

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
def kor():

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
                fig = plt.figure()   # Создание объекта Figure
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
                    for k in range(len(y_interp)-(N2-N1+M)):#перебираем первую границу окна от 0 до конца графика
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
                print("Границы интервала полученного автокорреляцией:",koef_kor[ind][0],'/',koef_kor[ind][1])
                print('Значение коэффициента на интервале полученным автокорреляцией:',max_koef)

                        
                plt.plot(x_val,x,color='grey', label="график первой функции")
                plt.plot(y_val,y, color='grey',label="график второй функции")
                
                #начинаем строить соответствие по ранее сохраненным границам y с максимальным коэффициентом корреляции
                i=N1#для графика x
                for j in range(koef_kor[ind][0],koef_kor[ind][1]+1,10):
                                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='green',lw=0.5)
                                i+=10
                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='green',lw=0.5, label="результат автокорреляции")
                
                #строим заданный пользователем интервал
                i=N1#для графика x
                for j in range(int(message4.get()),int(message5.get())+1,10):
                                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='lightblue',lw=0.5)
                                i+=10
                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='lightblue',lw=0.5, label="желаемый интервал")
                
                #строим среднее между тем, что ввел пользователь и результатом автокорреляции
                i=N1#для графика x
                for j in range((int(message4.get())+koef_kor[ind][0])//2,(int(message5.get())+koef_kor[ind][1])//2+1,10):
                                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='red')
                                i+=10
                plt.plot((x_val[i],y_val[j]),(x[i],y[j]),color='red', label="результат")

                #подсчет коэффициента автокорреляции на интервале введенном пользователем
                x_res=[]
                x_res_val=[]
                for i in range(int(message4.get()),int(message5.get())+1):
                    x_res.append(x_interval[i])
                    x_res_val.append(x_interp[i])
                    
                #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
                if len(x_res_val) != len(y_tek_val):
                    c1=np.linspace(min(min(x_res),min(y_tek)),max(max(x_res),max(y_tek)), (len(x_res)+len(y_tek))//2)
                    x_res_interp=np.interp(c1,x_res,x_res_val)
                    y_tek_interp=np.interp(c1,y_tek,y_tek_val)
                else:
                    x_res_interp=x_res_val
                    y_tek_interp=y_tek_val  
                print("Границы интервала введенного пользователем:",int(message4.get()),'/',int(message5.get()))
                print('Коэффициент корреляции на интервале введенном пользователем:',pearsonr(x_res_interp, y_tek_interp)[0])\
                      #коэффициент автокорреляции на коэффициента автокорреляции на интервале введенном пользователем

                #подсчет коэффициента автокорреляции на итоговом интервале
                x_res=[]
                x_res_val=[]
                for i in range((int(message4.get())+koef_kor[ind][0])//2,(int(message5.get())+koef_kor[ind][1])//2+1):
                    x_res.append(x_interval[i])
                    x_res_val.append(x_interp[i])
                    
                #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
                if len(x_res_val) != len(y_tek_val):
                    c1=np.linspace(min(min(x_res),min(y_tek)),max(max(x_res),max(y_tek)), (len(x_res)+len(y_tek))//2)
                    x_res_interp=np.interp(c1,x_res,x_res_val)
                    y_tek_interp=np.interp(c1,y_tek,y_tek_val)
                else:
                    x_res_interp=x_res_val
                    y_tek_interp=y_tek_val

                print("Границы результирующего интервала:",(int(message4.get())+koef_kor[ind][0])//2,'/',(int(message5.get())+koef_kor[ind][1])//2)
                print('Коэффициент корреляции на результирующем интервале:',pearsonr(x_res_interp, y_tek_interp)[0])\
                      #коэффициент автокорреляции на коэффициента автокорреляции на итоговом интервале
                plt.legend()    
                plt.show()



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

#желаемая левая граница второго графика
message4 = StringVar()

kor_entry4 = Entry(textvariable=message4,width=50)
kor_entry4.grid(row=3,column=1, padx=5, pady=5)
kor_label4 = Label(text="Введите желаемую левую границу второго графика:",width=50)
kor_label4.grid(row=3, column=0, sticky="w")

#желаемая правая граница второго графика
message5 = StringVar()

kor_entry5 = Entry(textvariable=message5,width=50)
kor_entry5.grid(row=4,column=1, padx=5, pady=5)
kor_label5 = Label(text="Введите желаемую правую границу второго графика:",width=50)
kor_label5.grid(row=4, column=0, sticky="w")

#кнопка корреляции
btn1=Button(tk, text='Построить соответсвие методом корреляции',width=50,command=kor)
btn1.grid(row=5,column=1, padx=5, pady=5, sticky="e")


