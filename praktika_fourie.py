from tkinter import *
import numpy as np
import random
from math import sqrt
from scipy.stats.stats import pearsonr
import pickle
from tkinter import messagebox
from math import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad # модуль для интегрирования
import numpy as np
import numpy.fft

def func_prem(t):# черный график
        a=float(message10.get())
        b=float(message11.get())
        if t>np.pi/b:
            p= (np.sin(a*5)-(np.sin(a*5)-1)*t)/(a+np.pi/10)
        else:
            p= (np.sin(b*5)-(np.sin(b*5)-1)*t)/(b+np.pi/10)
        return p

def func_black_koef(t,k,w):#функция для расчёта коэффициента b[k] для черного графика
         if t<np.pi:
                  y=func_prem(t)*np.sin(w*k*t)
         else:
                  y=-func_prem(t)*np.sin(w*k*t)
         return y

def koef_fourier_black(n1,n2):#коэффициенты фурье для красного графика
    T=np.pi
    w=2*np.pi/T # период и круговая частота
    c=10
    g=[]
    m=np.arange(0,c,1)
    b=[round(2*quad(func_black_koef, n1, n2, args=(k,w))[0]/T,3) for k in m]# интеграл для b[k], k -номер гармоники
    return b

              
def func_sin(t):# анализируемая функция
        p=np.sin(t)
        return p
    
        
def func_sin_koef(t,k,w):#функция для расчёта коэффициента b[k] у sin(x) 
         if t<np.pi:
                  y=func_sin(t)*np.sin(w*k*t)
         else:
                  y=-func_sin(t)*np.sin(w*k*t)
         return y

        
def koef_fourier_sin(n1,n2):#коэффициенты фурье для красного графика
    T=np.pi
    w=2*np.pi/T # период и круговая частота
    c=10
    g=[]
    m=np.arange(0,c,1)
    b=[round(2*quad(func_sin_koef, n1, n2, args=(k,w))[0]/T,3) for k in m]# интеграл для b[k], k -номер гармоники
    return b
      

def func(a,b):
    y=[sin(5*a),1,sin(5*b)]
    x=[a,pi/2,b]
    c1=np.linspace(a,b, int(message12.get()))
    y=np.interp(c1,x,y)
    return y
    
def func2(a,b):
    return [sin(i) for i in np.arange(a,b,(b-a)/float(message12.get()))]


##def func_1(t,k,w):# функция для расчёта коэффициента a[k] 
##         if t<np.pi:
##                  z=np.cos(t)*np.cos(w*k*t)
##         else:
##                  z=-np.cos(t)*np.cos(w*k*t)
##         return z
##        
def func_2(t,k,w):#функция для расчёта коэффициента b[k] 
         if t<np.pi:
                  y=np.cos(t)*np.sin(w*k*t)
         else:
                  y=-np.cos(t)*np.sin(w*k*t)
         return y

def fourie(n1,n2):
    T=np.pi
    w=2*np.pi/T # период и круговая частота
    c=10
    g=[]
    m=np.arange(0,c,1)
    b=[round(2*quad(func_2, n1, n2, args=(k,w))[0]/T,3) for k in m]# интеграл для b[k], k -номер гармоники
    return b
            

def draw():
    a=float(message10.get())
    b=float(message11.get())
    x=[a,1,b]
    x_val=[np.sin(5*a),np.pi/10,np.sin(5*b)]
    c1=np.linspace(a,b,200)
    x_val=np.interp(c1,x,x_val)
    x=np.arange(a,b,(b-a)/float(message12.get()))
    y_val=func2(a,b)
    y=x.copy()
    x_val=[i+3 for i in x_val]
    plt.plot(x_val,x)
    plt.plot(y_val,y, color="red")
    plt.show()

def kor():

    a=float(message10.get())
    b=float(message11.get())
##    x_val=[sin(5*a),1,sin(5*b)]
##    x=[a,np.pi/2,b]
##    x_val=[2.25,2.97,2.84]
##    x=[-9.98,-5.89,9.09]
    x_val=[4.25,4.98,4.66]
    x=[-20.18,-5.86,20.08]
    c1=np.linspace(a,b,int(message12.get()))
    x_val=np.interp(c1,x,x_val)
    x=np.arange(a,b,(b-a)/float(message12.get()))
    y_val=func2(a,b)
    y=x.copy()
    x_val=[i+2 for i in x_val]

    
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
                    x_tek.append(x[i])
                    x_tek_val.append(x_val[i])
                    
                x_tek_val=koef_fourier_black(N1,N2)
                x_tek=np.linspace(N1,N2,len(x_tek_val))
                y_tek=[]#отделили глубины на отрезке y
                y_tek_val=[]#отделили значения на отрезке y

                koef_kor=[]#список для хранения границ корреляции

                #перебираем график y учитывая отклонение M
                for j in range(N2-N1-M,N2-N1+M+1):#перебираем возможные размеры окна
                    for k in range(len(y_val)-j):#перебираем первую границу окна от 0 до конца графика
                                for i in range(k,k+j+1):
                                        y_tek.append(y[i])
                                        
                                y_tek_val=koef_fourier_black(k,k+j+1)
                                y_tek=np.linspace(k,k+j+1,len(y_tek_val))
                            
##                                print(len(x_tek),len(x_tek_val))
##                                print(len(y_tek),len(y_tek_val))
##                                #переинтерполируем два получивщихся окна(так как их размеры могут не совпадать)
##                                if len(x_tek_val) != len(y_tek_val):
##                                    c1=np.linspace(min(min(x_tek),min(y_tek)),max(max(x_tek),max(y_tek)), (len(x_tek)+len(y_tek))//2)
##                                    x_tek_interp=np.interp(c1,x_tek,x_tek_val)
##                                    y_tek_interp=np.interp(c1,y_tek,y_tek_val)
##                                    
##                                else:
##                                    x_tek_interp=x_tek_val
##                                    y_tek_interp=y_tek_val
                                sum=0
                                for i in range(len(x_tek_val)):
                                    sum+=abs(x_tek_val[i]-y_tek_val[i])
                                f = open('fourie.txt', 'a')
                                f.write(str(sum)+'\n')
                                #запишем коэффициенты корреляции для каждой получившейся пары окон
                                #0 и 1 элементы это границы окна y
                                #2 элемент это сам коэффициент
                                koef_kor.append([k,k+j,sum])
                                y_tek=[]

                #после заполнения всех возможных коэффициентов корреляции найдем максимальный

                min_koef=float('inf')
                ind=[]
                vse=0
                for i in koef_kor:
                    
                    if i[2]<min_koef:
                        min_koef=i[2]
                        ind=[]
                        ind.append(vse)
                    elif i[2]==min_koef:
                        ind.append(vse)
                    vse+=1
##                print(koef_kor[ind][0],koef_kor[ind][1],min_koef)




                plt.plot(x_val,x)

                j=0
                


                plt.plot(y_val,y, color="red")
                for i in ind:
                        plt.plot((x_val[N1],y_val[koef_kor[i][0]]),(x[N1],y[koef_kor[i][0]]),color='green')
                        plt.plot((x_val[N2],y_val[koef_kor[i][1]]),(x[N2],y[koef_kor[i][1]]),color='green')
                plt.show()



    
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
btn1=Button(tk, text='Построить соответсвие методом корреляции',width=50,command=kor)
btn1.grid(row=6,column=1, padx=5, pady=5, sticky="e")

#границы графиков
message10 = StringVar()
entry_sin = Entry(textvariable=message10,width=25)
entry_sin.grid(row=4,column=1, padx=30, pady=5,sticky="w")

message11 = StringVar()
entry_sin2 = Entry(textvariable=message11,width=25)
entry_sin2.grid(row=4,column=1, padx=30, pady=5,sticky="e")

label_sin = Label(text="Введите пределы по x:",width=50)
label_sin.grid(row=4, column=0, sticky="w")

# количество точек на графике
message12 = StringVar()
entry_sin3 = Entry(textvariable=message12,width=50)
entry_sin3.grid(row=5,column=1, padx=30, pady=5)

label_sin2 = Label(text="Введите количество точек:",width=50)
label_sin2.grid(row=5, column=0, sticky="w")

btn5=Button(tk, text='Построить кривые',width=50,command=draw)
btn5.grid(row=13,column=1, padx=5, pady=5, sticky="e")
