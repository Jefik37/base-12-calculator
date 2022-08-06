from math import sqrt
from math import factorial as fact
from math import floor
import subprocess
import tkinter as tk

# Program made By Jefik
# Link on GitHub: https://github.com/Jefik37/base-12-calculator

def tentobase(numog):
    numog=str(numog)
    base=12
    erro=False
    condicao=[]
    if numog[0]=='-':
        numog=str(float(numog)*(-1))
        condicao.append('negativo')
    num=[] #lista para guardar os valores inteiros
    decimais1=[] #lista para guardar os valores decimais, esta linha serve somente para não dar erro no return
    if '.' in numog: #checar decimais
        numseparado=numog.split('.') #separar inteiros e decimais
        numog=numseparado[0] #definir inteiros
        decimais=int(numseparado[1])/10**(len(numseparado[1])) #definir decimais e separar casas em lista

        decimais1=[';'] #lista para guardar os valores decimais
        while decimais!=int(decimais) and len(decimais1)<17: #calcular os decimais
            decimais*=base
            decimais1.append(str(floor(decimais))) #adicionar o valor inteiro da multiplicação na lista
            if decimais!=int(decimais): #se ainda tiver algum decimal:
                decimais-=floor(decimais) #remover a parte inteira do número
        for i in range (1, len(decimais1)): #converter números maiores que 10 em letras e depois em string
            if int(decimais1[i])>=10:
                decimais1[i]=chr(int(decimais1[i])+55)
            decimais1[i]=str(decimais1[i])
        decimais1=''.join(decimais1) #transformar a lista em uma string
    try:
        numog=int(numog)
    except:
        erro=True
    if not erro:
        if numog==int(numog):
            while numog//base!=0: #calcular os inteiros
                num.append(numog%base) #adicionar o resto na lista de inteiros
                numog=numog//base
            num.append(numog%base)
            for i in range (0, len(num)): #converter números maiores que 10 em letras e inverter a lista
                if num[i]>=10:
                    num[i]=chr(num[i]+55)
                num[i]=str(num[i])
            if 'negativo' in condicao: #adicionar o sinal de negativo se o número for negativo
                num.append('-')
            num=''.join(num[::-1]) #transformar a lista em uma string
        if decimais1!=[]:
            return f'{num}{decimais1}'
        elif not erro:
            return num
"""    else:
        return ' '"""

def basetoten(numog):
    numog=str(numog)
    base=12
    erro=False
    newnum=0 #criar variável para o resultado
    num1=numog.upper() #deixar tudo em minúsculo
    condicao=[]

    #if '√' in num1:
    #    num1=num1.replace('√', '')
    #    condicao.append('raiz')
    if '!' in num1:
        num1=num1.replace('!', '')
        condicao.append('fatorial')

    if ';' in num1: #checar decimais
        numseparado=num1.split(';') #separar inteiros e decimais
        num1=numseparado[0] #definir inteiros
        decimais=list(numseparado[1]) #definir decimais e separar casas em lista

        for i in range (0, len(decimais)): #converter decimais em base 10
            if not decimais[i].isdigit(): #se for letra:
                decimais[i]=str(ord(decimais[i])-55) #converter em número
            if int(decimais[i])>=base: #caso tenha alguma letra inválida:
                erro=True
            newnum+=float(decimais[i])*base**(-i-1) #valor+=dígito*(a sua posição). ex 0.a(base 12)=0.10*12^-1(base 10)
    num=list(num1) #separar casas da parte inteira em lista
    for i in range (0, len(num)): #calcular os inteiros
        if not num[i].isdigit(): #se for letra:
            num[i]=str(ord(num[i])-55) #converter em número
        if int(num[i])>=base: #caso tenha alguma letra inválida:
            erro=True
        newnum+=int(num[i])*base**(len(num)-i-1) #valor+=dígito*(a sua posição). ex b(base 12)=11*12^0(base 10)
    #if 'raiz' in condicao:
    #    newnum=f'({newnum})**(1/2)'
    if 'fatorial' in condicao:
        newnum=fact(newnum)
    if not erro:
        return str(newnum)
"""    else:
        return ' '"""

def convertersimb(x):
    sinais=['÷', '^', '↊','↋', '=', '√', '²', '%']
    sinais2=['/', '**', 'a', 'b', '', 'sqrt', '**(2)', '/(100)']
    for i in range (0, len(sinais)):
        x=x.replace(sinais[i], sinais2[i])
    return(x)


def consertarparenteses(x):
    x=list(x)
    for i in range (1, len(x)-1):
        if x[i]=='(':
            if x[i-1].isnumeric() or x[i-1]=='a' or x[i-1]=='b':
                x[i]='*('
        if x[i]==')':
            if x[i+1].isnumeric() or x[i+1]=='a' or x[i+1]=='b':
                x[i]=')*'
    return(''.join(x))

def separarnum(x):
    sinais='()*+-/sqrt'
    numeros='1234567890ABab;'
    simb=x
    numb=x
    for i in range(0, len(sinais)):
        numb=numb.replace(sinais[i], ' ')
    numb=numb.replace(' ', ' @ ')
    numb=numb.split()
    for i in range (0, len(numb)):
        numb[i]=numb[i].replace('@', ' ')
        if numb[i]!=' ':
            numb[i]=basetoten(numb[i])
    #numb=''.join(numb)
    #numb=list(numb)
    for i in range(0, len(numeros)):
        simb=simb.replace(numeros[i], ' ')
    print(numb)
    print(simb)
    for i in range(0, len(numb)-1):
        if simb[i]=="t": #garantir que a função sqrt() funcione
            a=i+1
            while numb[a]==' ' or a==len(numb): #enquanto não achar um número na lista de números, o programa vai continuar procurando
                a+=1
            if numb[a]!=' ': #se encontrar:
                numb[a]='('+numb[a]+')' #
    simb=simb.split()
    simb=''.join(simb)
    simb=list(simb)
    return(numb, simb) ####


def juntar(numb, simb):
    numb=list(numb)
    simbolo=0
    for i in range(0, len(numb)):
        if numb[i]==' ':
            numb[i]=simb[simbolo]
            simbolo+=1
    return(''.join(numb))

def atualizarvisor(x): ########################################################################
    if visor.get()=='':
        preview['text']=''
    if visor.get()[0]=='=':
        visor.delete(0)
    string=visor.get()
    try: #garantir que só seja exibido o resultado caso ele seja válido
        string=convertersimb(string)
        string=(consertarparenteses(string))
        string=separarnum(string)
        quantidadenumeros=len(string[0])
        simbolosusados=string[1]
        string=juntar(string[0], string[1])
        try:
            string=f'{eval(string):.17f}'
        except:
            ...
        string=tentobase(string)
        #string=string[:len(visor.get())]
        string=string.replace('A', '↊')
        string=string.replace('B', '↋')

        if len(string)<37:
            preview.config(width=(len(string)))
        else:
            preview.config(width=(37))

        if quantidadenumeros<=1 and '!' not in simbolosusados: #evita de mostrar preview do tipo 5 = 5
            preview['text']=''
        else:
            preview['text']='=',string

        preview1=preview.cget('text') #tirar ; no final da preview se não tiver dígitos depois
        if preview1[len(preview1)-1:len(preview1)]==';':
            preview['text']=preview1[:-1]

    except AttributeError:
        preview['text']=''
def clear():
    if visor.get()!='':
        visor.delete(0, tk.END)
    else:
        preview['text']=''
        historico['text']=''
    atualizarvisor('')

def exponentiation():
    visor.insert(tk.INSERT, '^')
    atualizarvisor('')


def copy():
    texto=preview.cget('text')
    texto=(texto[:-len(texto)+1:-1])[::-1]
    texto=texto.replace('↊', 'A')
    texto=texto.replace('↋', 'B')
    cmd='echo '+texto.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def semi():
    if visor.get()=='':
        visor.insert(tk.END, '0')
    visor.insert(tk.INSERT, ';') 
    atualizarvisor('')

def delete():
    position = visor.index(tk.INSERT)
    visor.icursor(position-1)
    visor.delete("insert")
    atualizarvisor('')

def moreless():
    if visor.get()!='':
        num=visor.get()
        num=f'({num})*(-1)'
        visor.insert(0, '(')
        visor.insert(tk.END, ')*(-1)')
        atualizarvisor('')

def square():
    visor.insert(tk.INSERT, '²')
    atualizarvisor('')

def squareroot():
    visor.insert(tk.INSERT, '√')
    atualizarvisor('')

def percent():
    visor.insert(tk.INSERT, '%')
    atualizarvisor('')

def division():
    visor.insert(tk.INSERT, '÷')
    atualizarvisor('')

def nine():
    visor.insert(tk.INSERT, '9')
    atualizarvisor('')

def dek():
    visor.insert(tk.INSERT, '↊')
    atualizarvisor('')

def el():
    visor.insert(tk.INSERT, '↋')
    atualizarvisor('')

def inverse():
    visor.insert(tk.INSERT, '^(-1)')
    atualizarvisor('')

def multiplication():
    visor.insert(tk.INSERT, '*')
    atualizarvisor('')

def six():
    visor.insert(tk.INSERT, '6')
    atualizarvisor('')

def seven():
    visor.insert(tk.INSERT, '7')
    atualizarvisor('')

def eight():
    visor.insert(tk.INSERT, '8')
    atualizarvisor('')

def factorial():
    visor.insert(tk.INSERT, '!')
    atualizarvisor('')

def minus():
    visor.insert(tk.INSERT, '-')
    atualizarvisor('')

def three():
    visor.insert(tk.INSERT, '3')
    atualizarvisor('')

def four():
    visor.insert(tk.INSERT, '4')
    atualizarvisor('')

def five():
    visor.insert(tk.INSERT, '5')
    atualizarvisor('')

def parleft():
    visor.insert(tk.INSERT, '(')
    atualizarvisor('')

def plus():
    if visor.index(tk.INSERT)!='+':
        visor.insert(tk.INSERT, '+')
    atualizarvisor('')

def zero():
    visor.insert(tk.INSERT, '0')
    atualizarvisor('')

def one():
    visor.insert(tk.INSERT, '1')
    atualizarvisor('')

def two():
    visor.insert(tk.INSERT, '2')
    atualizarvisor('')

def parright():
    visor.insert(tk.INSERT, ')')
    atualizarvisor('')

def equal():
    if preview.cget('text')!='':
        tamanhonovo=len(visor.get())
        if tamanhonovo<37: #garante que o histórico não aumente a tela
            historico.config(width=tamanhonovo)
        else:
            historico.config(width=37)
        if historico.cget('text')!=visor.get():
            historico['text']=visor.get()
            visor.delete(0,tk.END)
            visor.insert(0, (preview['text']))
            visor.delete(1)
            preview['text']=''

def equalenter(x):
    equal()


window=tk.Tk()
window.title("Base 12 Calculator")
window.resizable(False, False)
window.bind("<Key>", atualizarvisor)
window.bind("<Button-1>", atualizarvisor)

fundo='#1d2029'
teclas='#30323c'
teclas2='#373b47'
teclas2act='#262830'
corigual='#4cc2ff'
corigualact='#42a1d4'
corsimbigual='#2a6788'
window.config(bg=fundo)
window.maxsize(498, 0)

commands=[[clear, exponentiation, parleft, parright, delete],
        [moreless, square, squareroot, percent, division],
        [nine, dek, el, inverse, multiplication],
        [six, seven, eight, factorial, minus],
        [three, four, five, semi, plus],
        [zero, one, two, copy, equal]]

frm_visor=tk.Frame(borderwidth=3, width=20, bg=fundo)
frm_visor.grid(row=0, column=0)

preview=tk.Label(master=frm_visor, height=1, font='Calibre 16 bold', borderwidth=0, bg=fundo, fg=teclas, text='')
preview.grid(row=2, column=0, sticky='se')

visor=tk.Entry(master=frm_visor, justify='right', width=17, font='Calibre 38 bold', borderwidth=0, bg=fundo, fg='white')
visor.grid(row=1, column=0)
window.bind("<Return>", equalenter)

historico=tk.Label(master=frm_visor, height=1, font='Calibre 16 bold', borderwidth=0, bg=fundo, fg='white', text='')
historico.grid(row=0, column=0, sticky='ne')

frm_keys=tk.Frame(borderwidth=3, height=400, width=500, bg=fundo)
frm_keys.grid(row=2, column=0)


keys=[['C', 'xʸ', '(', ')', '⌫'],
        ['±', 'x²', '√x', '%', '÷'],
        ['9', '↊', '↋','1/x', '*'],
        ['6', '7', '8', 'x!', '-'],
        ['3', '4', '5', ';', '+'],
        ['0', '1', '2', '📋', '=']]


for i in range (0, len(keys)):
    for j in range (0, len(keys[0])):
        key=tk.Button(master=frm_keys, text=keys[i][j], height=2, width=6, font='Calibre 19',
        bg=teclas, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=commands[i][j])
        if keys[i][j] in '1234567890↊↋':
            key.config(bg=teclas2, activebackground=teclas2act, activeforeground='white')
        if keys[i][j]=='=':
            key.config(bg=corigual, fg='black', activebackground=corigualact, activeforeground=corsimbigual)
        key.grid(row=i, column=j, padx=1, pady=1)

window.mainloop()
