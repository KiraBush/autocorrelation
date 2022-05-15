import turtle as t
axiom='F++F++F'#начальное поколение
s=''#новое поколение

for j in range(20):
    for i in axiom:
        if i=='F':
            s=s+'F-F++F-F'
        else:
            s=s+i
    axiom=s
    s=''
t.bgcolor('black')
t.pencolor('blue')
t.tracer(0)
for i in axiom:
    if i=='F':
        t.forward(1)
    elif i=='+':
        t.left(60)
    else:
        t.right(60)

