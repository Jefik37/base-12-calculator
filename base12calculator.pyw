from math import sqrt
from math import factorial as fact
from math import log as ln

from math import floor
from math import ceil as cil

from math import sin as sinr
from math import cos as cosr
from math import tan as tanr

from math import sinh as sinhr
from math import cosh as coshr
from math import tanh as tanhr

from math import asin as asinr
from math import acos as acosr
from math import atan as atanr

from math import asinh as asinhr
from math import acosh as acoshr
from math import atanh as atanhr

from math import radians
from math import degrees
import subprocess
import tkinter as tk

# Program made By Jefik
# Link on GitHub: https://github.com/Jefik37/base-12-calculator

e12='2;8752360698219↋'
pi12='3;184809493↋9186'

def tentobase(numog):
    numog=str(numog)
    if numog=='2.71828182845904420':
        return(e12)
    elif numog=='3.14159265358979267':
        return(pi12)
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
        if len(decimais1)>1:
            return f'{num}{decimais1}'
        elif not erro:
            return f'{num}'

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
    if not erro:
        return str(newnum)

radianos=True

trig=['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh']

for i in trig:
    exec(f"""def {i}(x):
    if radianos:
        return({i}r(x))
    else:
        return({i}r(radians(x)))""")

trig2=['asin', 'acos', 'atan', 'asinh', 'acosh', 'atanh']

for i in trig2:
    exec(f"""def {i}(x):
    if radianos:
        return({i}r(x))
    else:
        return(degrees({i}r(x)))""")

def degree():
    if radianos:
        globals()['radianos']=False
        botaodeg.configure(text= 'deg °', bg=teclas3act, activebackground=teclas3)

    else:
        globals()['radianos']=True
        botaodeg.configure(text='rad π', bg=teclas, activebackground=teclas2)
    atualizarvisor()

def log(x, y=10):
    return float((ln(float(basetoten(x)), float(basetoten(y)))))

def root(x, y=2):
    return(float( basetoten(x) )**(1/ float(basetoten(y)) ))

def convertersimb(x):
    sinais=['÷', '^', '²', 'A', 'B', ' ', ')(', 'ceil']
    sinais2=['/', '**', '**(2)', '↊', '↋', '', ')*(', 'cil']

    x=''.join(x)

    for i in range (0, len(sinais)):
        x=x.replace(sinais[i], sinais2[i])
    return(x)

def consertarparenteses(x):
    x=list(x)
    for i in range (1, len(x)-1):
        if x[i]=='(':
            if x[i-1].isnumeric() or x[i-1]=='A' or x[i-1]=='B':
                x[i]='*('
        if x[i]==')':
            if x[i+1].isnumeric() or x[i+1]=='A' or x[i+1]=='B':
                x[i]=')*'

    return(''.join(x))

def separarnum(x):
    numeros='0123456789↊↋;. eπ'

    simbolosproblematicos=['√', 'ᴇ', 'ln', 'log', 'fact', 'root', 'π', 'e',
    'sinh', 'cosh', 'tanh', 'sin', 'cos', 'tan', 'abs', 'cil', 'floor', 'a']

    for i in simbolosproblematicos:
        x=x.replace(i, '@'+i)
    
    x=list(x)
    for i in range(1, len(x)):
        if x[i]=='@' and x[i-1] in numeros:
            x[i]='*'
    x=''.join(x)
    x=x.replace('@', '')
    x=x.replace('π', pi12)
    x=x.replace('e', e12)

    print(f'1{x = }')
    x2=[]
    for i in range(0, len(x)-1):
        if (x[i] in numeros and x[i+1] not in numeros) or (x[i] not in numeros and x[i+1] in numeros):
            x2.append(x[i]+' ')
        else:
            x2.append(x[i])
    
    x2.append(x[len(x)-1])
    x=x2
    print(f'2{x = }')
    x=''.join(x)
    x=x.split(' ')
    listanumeros=[]
    for i in range(0, len(x)): #converter pra base 12 e salvar os números em uma lista
        num=True
        for j in x[i]:
            if j not in numeros:
                num=False
        if num:
            x[i]=x[i].replace('↊', 'a')
            x[i]=x[i].replace('↋', 'b')
            listanumeros.append(x[i])
            x[i]=basetoten(x[i])

    c=x
    x=(''.join(x))
    x=x.replace('√', 'sqrt')
    x=x.replace('ᴇ', '12**')
    return(x, listanumeros, c)

def atualizarvisor(x=None):
    if visor.get()=='':
        preview['text']=''
    string=visor.get()
    try: #garantir que só seja exibido o resultado caso ele seja válido
        string=convertersimb(string)
        string=(consertarparenteses(string))
        string=separarnum(string)[0]
        numerosequacao=separarnum(string)[1]
        equacaopython=separarnum(string)[2]
        numoperacoes=len(equacaopython)-len(numerosequacao)
        string=str(string)
        print(f'{string = }')
        try:
            string=f'{eval(string):.14f}'
        except Exception as e:
            preview.delete(0, tk.END)
        print(f'b10 {string = }')
        string=tentobase(string)
        #string=string[:len(visor.get())]
        string=string.replace('A', '↊')
        string=string.replace('B', '↋')

        if string=='-0':
            string='0'

        if len(string)<35:
            preview.config(width=(len(string)+2))
        else:
            preview.config(width=(37))

        if numoperacoes>0 or 'π' in visor.get() or 'e' in visor.get():
            preview['text']='=',string
        else:
            preview['text']=''

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

def moreless():
    if visor.get()!='':
        visor.insert(0, '(')
        visor.insert(tk.END, ')*(-1)')
        atualizarvisor('')

def minus():
    a=visor.get()
    b=visor.index(tk.INSERT)
    if a[b-1]!='-':
        visor.insert(tk.INSERT, '-')
    atualizarvisor('')

def plus():
    a=visor.get()
    b=visor.index(tk.INSERT)
    if a[b-1]!='+':
        visor.insert(tk.INSERT, '+')
    atualizarvisor('')

def copy():
    texto=preview.cget('text')
    if texto!='':
        texto=(texto[:-len(texto)+1:-1])[::-1]
        texto=texto.replace('↊', 'A')
        texto=texto.replace('↋', 'B')
    else:
        texto=visor.get()
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

def equal(x=None):
    if preview.cget('text')!='':
        tamanhonovo=len(visor.get())
        if tamanhonovo<35: #garante que o histórico não aumente a tela
            historico.config(width=tamanhonovo+2)
        else:
            historico.config(width=37)
        if historico.cget('text')!=visor.get():
            historico['text']=visor.get()+' ='
            visor.delete(0,tk.END)
            visor.insert(0, (preview['text']))
            visor.delete(0)
            preview['text']=''

        #atualizar lista do histórico
        janelahistorico.configure(state='normal') 
        historiconovo=historico['text']
        janelahistorico.insert(tk.END, (historiconovo)[0:len(historiconovo)-1]+'='+visor.get()+'\n\n')
        janelahistorico.configure(state='disabled')

def abrirhistorico():
    if janelahistorico.grid_info()=={}:
        janelahistorico.grid(row=2, column=0, sticky='s')
        janelahistorico.tag_configure('sometag', justify='right')
        janelahistorico.tag_add('sometag', 1.0, 'end')
    else:
        janelahistorico.grid_remove()

botoesbasicos=[['inverse', '^(-1)'], ['multiplication', '*'], ['factorial', 'fact('], ['parleft', '('],
['parright', ')'], ['square', '²'], ['squareroot', '√('], ['percent', '%'], ['division', '÷'], ['exponentiation', '^'],
['zero', '0'], ['one', '1'], ['two', '2'], ['three', '3'], ['four', '4'], ['five', '5'], ['six', '6'],
['seven', '7'], ['eight', '8'], ['nine', '9'], ['dek', '↊'], ['el', '↋'], ['adde', 'e'], ['addpi', 'π'],
['mod', '%'], ['addlogyx', 'log(x, y)'], ['exp', 'ᴇ'], ['addcomma', ','], ['addroot', 'root(x, y)'], ['addlnx', 'ln('],
['addsin', 'sin('], ['addcos', 'cos('], ['addtan', 'tan('], ['modulo', 'abs('], ['addceil', 'ceil('], ['addfloor', 'floor('],
['addsinh', 'sinh('], ['addcosh', 'cosh('], ['addtanh', 'tanh('], ['addasin', 'asin('], ['addacos', 'acos('], ['addatan', 'atan('],
['addasinh', 'asinh('], ['addacosh', 'acosh('], ['addatanh', 'atanh(']]

for i in botoesbasicos:
    exec(f'''def {i[0]}():
    visor.insert(tk.INSERT, '{i[1]}')
    atualizarvisor("")''')

window=tk.Tk()
window.title("Base 12 Calculator")
window.resizable(False, False)
window.bind("<Key>", atualizarvisor)
window.bind("<Button-1>", atualizarvisor)

fundo='#1d2029'
teclas='#30323c'
teclas2='#373b47'
teclas3='#383f53'
teclas3act='#303b5a'
teclas2act='#262830'
teclashyp='#f8eea7'
corigual='#4cc2ff'
corigualact='#42a1d4'
corsimbigual='#2a6788'
window.config(bg=fundo)
window.maxsize(498, 0)

frm_cabecalho=tk.Frame(borderwidth=3, width=20, bg=fundo)
frm_cabecalho.grid(row=0, column=0)

botaohistorico=tk.Button(master=frm_cabecalho, text='↺', font='Calibre 19',
        bg=fundo, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=abrirhistorico)
botaohistorico.grid(row=0, column=2)

botaomenu=tk.Button(master=frm_cabecalho, text='📋', font='Calibre 19', #≡
        bg=fundo, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=copy)
botaomenu.grid(row=0, column=0)

tab_control = tk.Label(master=frm_cabecalho, bg=fundo)
tab_control.grid(row=0, column=1, padx=200)

frm_visor=tk.Frame(borderwidth=3, width=20, bg=fundo)
frm_visor.grid(row=1, column=0)

preview=tk.Label(master=frm_visor, height=1, font='Calibre 16 bold', borderwidth=0, bg=fundo, fg=teclas, text='')
preview.grid(row=2, column=0, sticky='se')

visor=tk.Entry(master=frm_visor, justify='right', width=17, font='Calibre 38 bold', borderwidth=0, bg=fundo, fg='white')
visor.grid(row=1, column=0)
window.bind("<Return>", equal)

historico=tk.Label(master=frm_visor, height=1, width=37, font='Calibre 16 bold', borderwidth=0, bg=fundo, fg='white', text='')
historico.grid(row=0, column=0, sticky='ne')

frm_keys=tk.Frame(borderwidth=3, height=400, width=500, bg=fundo)
frm_keys.grid(row=2, column=0)



botaopontovirgula=tk.Button()
botaoraiz=tk.Button()
botaoquadrado=tk.Button()
shiftativado=False
hypativado=False


def hyp(x=None):
    if not globals()['hypativado']:
        cor=teclashyp
        globals()['hypativado']=True
        botaohyp.configure(bg=teclas3act, activebackground=teclas3, fg=cor, activeforeground=cor)

        if not shiftativado:
            botoes=['sin', 'sinh', 'addsinh'], ['cos', 'cosh', 'addcosh'], ['tan', 'tanh', 'addtanh']
        else:
            botoes=['sin', 'sinh⁻¹', 'addasinh'], ['cos', 'cosh⁻¹', 'addacosh'], ['tan', 'tanh⁻¹', 'addatanh']
    else:
        globals()['hypativado']=False
        botaohyp.configure(bg=teclas, activebackground=teclas2, fg='white', activeforeground='white')
        cor='white'

        if not shiftativado:
            botoes=['sin', 'sin', 'addsin'], ['cos', 'cos', 'addcos'], ['tan', 'tan', 'addtan']
        else:
            botoes=['sin', 'sin⁻¹', 'addasin'], ['cos', 'cos⁻¹', 'addacos'], ['tan', 'tan⁻¹', 'addatan']

    for i in botoes:
        exec(f"botao{i[0]}.configure(text='{i[1]}', command={i[2]}, fg='{cor}')")

def shift(x=None):
    if not globals()['shiftativado']:
        globals()['shiftativado']=True
        botaoshift.configure(bg=teclas3act, activebackground=teclas3)

        botoes1=[['quadrado', 'xʸ', 'exponentiation'], ['raiz', 'ʸ√x', 'addroot'],
        ['lnx', 'logᵧx', 'addlogyx'], ['ceil', '⌊x⌋', 'addfloor'], ['pontovirgula', ',', 'addcomma']]

        botoestrig=['sin', 'sin⁻¹', 'addasin'], ['cos', 'cos⁻¹', 'addacos'], ['tan', 'tan⁻¹', 'addatan']
        botoestrigh=['sin', 'sinh⁻¹', 'addasinh'], ['cos', 'cosh⁻¹', 'addacosh'], ['tan', 'tanh⁻¹', 'addatanh']
        
        cores=['teclas3', 'teclas3act', 'teclashyp']

    else:
        globals()['shiftativado']=False
        botaoshift.configure(bg=teclas, activebackground=teclas2)

        botoes1=[['quadrado', 'x²', 'square'], ['raiz', '²√x', 'squareroot'],
        ['lnx', 'lnx', 'addlnx'], ['ceil', '⌈x⌉', 'addceil'], ['pontovirgula', ';', 'semi']]

        botoestrig=['sin', 'sin', 'addsin'], ['cos', 'cos', 'addcos'], ['tan', 'tan', 'addtan']
        botoestrigh=['sin', 'sinh', 'addsinh'], ['cos', 'cosh', 'addcosh'], ['tan', 'tanh', 'addtanh']
        
        cores=['teclas', 'teclas2', '']

    for i in botoes1:
        exec(f"botao{i[0]}.configure(text='{i[1]}', command={i[2]}, bg={cores[0]}, activebackground={cores[1]})")

    if globals()['hypativado']:
        for i in botoestrigh:
            exec(f"botao{i[0]}.configure(text='{i[1]}', command={i[2]}, bg={cores[0]}, activebackground={cores[1]})")
    else:
        for i in botoestrig:
            exec(f"botao{i[0]}.configure(text='{i[1]}', command={i[2]}, bg={cores[0]}, activebackground={cores[1]})")

keys=[[['¹⁄ₓ', 'inverso', inverse], ['(', 'abreparenteses', parleft], [')', 'fechaparentess', parright], ['C', 'C', clear], ['⌫', 'deleta', delete]],
[['hyp', 'hyp', hyp], ['±', 'maismenos', moreless], ['π', 'pi', addpi], ['e', 'e', adde], ['exp', 'exp', exp]],
[['shift', 'shift', shift], ['mod', 'mod', mod], ['x!', 'fatorial', factorial],  ['|x|', 'modulo', modulo], ['÷', 'divisao', division]],
[['x²', 'quadrado', square], ['²√x', 'raiz', squareroot], ['lnx', 'lnx', addlnx], ['⌈x⌉', 'ceil', addceil], ['*', 'vezes', multiplication]], #['logᵧx', 'logyx', addlogyx]
[['sin', 'sin', addsin], ['9', '9', nine], ['↊', 'dec', dek], ['↋', 'el', el], ['-', 'menos', minus]],
[['cos', 'cos', addcos], ['6', '6', six], ['7', '7', seven], ['8', '8', eight], ['+', 'mais', plus]],
[['tan', 'tan', addtan], ['3', '3', three], ['4', '4', four], ['5', '5', five], [';', 'pontovirgula', semi]],
[['rad π', 'deg', degree], ['0', '0', zero], ['1', '1', one], ['2', '2', two], ['=', 'igual', equal]]]

for i in range (0, len(keys)):
    for j in range (0, len(keys[0])):
        exec(f"""botao{keys[i][j][1]}=tk.Button(master=frm_keys, text=keys[i][j][0], height=1, width=6, font='Calibre 19',
        bg=teclas, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=keys[i][j][2])""")
        if keys[i][j][0] in '1234567890↊↋':
            exec(f"""botao{keys[i][j][1]}.config(bg=teclas2, activebackground=teclas2act, activeforeground='white')""")
        if keys[i][j][0]=='=':
            exec(f"""botao{keys[i][j][1]}.config(bg=corigual, fg='black', activebackground=corigualact, activeforeground=corsimbigual)""")
        exec(f"""botao{keys[i][j][1]}.grid(row=i, column=j, padx=1, pady=1)""")



janelahistorico=tk.Text(master=window, width=35, height=14, font='Calibre 19', bg=teclas, fg='white')
window.mainloop()
