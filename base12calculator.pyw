from math import factorial, sqrt
from math import factorial as fact
from math import floor
from math import log as ln
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
    #if 'raiz' in condicao:
    #    newnum=f'({newnum})**(1/2)'
    #if 'fatorial' in condicao:
        #newnum=fact(newnum)
    if not erro:
        return str(newnum)

def log(x, y=10):
    return float((ln(float(basetoten(x)), float(basetoten(y)))))

def root(x, y=2):
    return(float( basetoten(x) )**(1/ float(basetoten(y)) ))

def convertersimb(x):

    sinais=['÷', '^', '²', 'A', 'B', ' ', 'π', 'e', ')(']
    sinais2=['/', '**', '**(2)', '↊', '↋', '', pi12, e12, ')*(']
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
    numeros='0123456789↊↋;. eπ'

    simbolosproblematicos=['√', 'ᴇ', 'ln', 'log', 'fact', 'root']

    for i in simbolosproblematicos:
        if i!='e' or i!='π':
            x=x.replace(i, 'substituir'+i+'substituir')
    
    x=x.split('substituir')
    x=list(x)
    while '' in x:
        x.remove('')
    for i in range(1, len(x)): #converter casos como 5sqrt(a) para 5*sqrt(a)
        if x[i] in simbolosproblematicos and x[i-1] in numeros:
            x.insert(i, '*')
    x=''.join(x)
    
    x2=[]
    for i in range(0, len(x)-1):
        if (x[i] in numeros and x[i+1] not in numeros) or (x[i] not in numeros and x[i+1] in numeros):
            x2.append(x[i]+' ')
        else:
            x2.append(x[i])
    
    x2.append(x[len(x)-1])
    x=x2
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

    if len(x)==2 and x[0] in simbolosproblematicos:
        x[1]='('+x[1]+')'
    else:
        for i in range (0, len(x)-1): #arrumar raíz
            if '√' in x[i] or 'ln' in x[i] or 'ᴇ' in x[i]:
                x[i+1]='('+x[i+1]+')'
    

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
            string=f'{eval(string):.17f}'
        except:
            string=eval(string)
        string=tentobase(string)
        #string=string[:len(visor.get())]
        string=string.replace('A', '↊')
        string=string.replace('B', '↋')

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

def exponentiation():
    visor.insert(tk.INSERT, '^')
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
        if tamanhonovo<36: #garante que o histórico não aumente a tela
            historico.config(width=tamanhonovo+1)
        else:
            historico.config(width=37)
        if historico.cget('text')!=visor.get():
            historico['text']=visor.get()+'='
            visor.delete(0,tk.END)
            visor.insert(0, (preview['text']))
            visor.delete(0)
            preview['text']=''

        #atualizar lista do histórico
        janelahistorico.configure(state='normal') 
        historiconovo=historico['text']
        janelahistorico.insert(tk.END, (historiconovo)[0:len(historiconovo)-1]+' ='+visor.get()+'\n\n')
        janelahistorico.configure(state='disabled')

def abrirhistorico():
    if janelahistorico.grid_info()=={}:
        janelahistorico.grid(row=2, column=0, sticky='s')
        janelahistorico.tag_configure('sometag', justify='right')
        janelahistorico.tag_add('sometag', 1.0, 'end')
    else:
        janelahistorico.grid_remove()

botoesbasicos=[['inverse', '^(-1)'], ['multiplication', '*'], ['factorial', 'fact('], ['parleft', '('],
['parright', ')'], ['square', '²'], ['squareroot', '√'], ['percent', '%'], ['division', '÷'],
['zero', '0'], ['one', '1'], ['two', '2'], ['three', '3'], ['four', '4'], ['five', '5'], ['six', '6'],
['seven', '7'], ['eight', '8'], ['nine', '9'], ['dek', '↊'], ['el', '↋'], ['adde', 'e'], ['addpi', 'π'],
['mod', '%'], ['addlogyx', 'log(x, y)'], ['addlnx', 'ln'], ['exp', 'ᴇ'], ['addcomma', ','], ['addroot', 'root(x, y)']]

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
teclas2act='#262830'
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

botaomenu=tk.Button(master=frm_cabecalho, text=' ', font='Calibre 19', #≡
        bg=fundo, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=...)
botaomenu.grid(row=0, column=0)

tab_control = tk.Label(master=frm_cabecalho, bg=fundo)
tab_control.grid(row=0, column=1, padx=208)

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
def shift(x=None):
    if not globals()['shiftativado']:
        globals()['shiftativado']=True
        botaopontovirgula.configure(text=',', command=addcomma, bg=teclas2)
        botaoraiz.configure(text='ʸ√x', command=addroot, bg=teclas2)
        botaoquadrado.configure(text='xʸ', command=exponentiation, bg=teclas2)
    else:
        globals()['shiftativado']=False
        botaopontovirgula.configure(text=';', command=addcomma, bg=teclas)
        botaoraiz.configure(text='²√x', command=squareroot, bg=teclas)
        botaoquadrado.configure(text='x²', command=square, bg=teclas)



keys=[[['📋', 'botaocopia', copy], ['(', 'botaoabreparenteses', parleft], [')', 'botaofechaparentess', parright], ['C', 'botaoC', clear], ['⌫', 'botaodeleta', delete]],
[['mod', 'botaomod', mod], ['±', 'botaomaismenos', moreless], ['π', 'botaopi', addpi], ['e', 'botaoe', adde], ['exp', 'botaoexp', exp]],
[['x!', 'botaofatorial', factorial], ['¹⁄ₓ', 'botaoinverso', inverse], ['logᵧx', 'botaologyx', addlogyx], ['lnx', 'botaolnx', addlnx], ['÷', 'botaodivisao', division]],
[['9', 'botao9', nine], ['↊', 'botaodec', dek], ['↋', 'botaoel', el], ['x²', 'botaoquadrado', square], ['*', 'botaovezes', multiplication]],
[['6', 'botao6', six], ['7', 'botao7', seven], ['8', 'botao8', eight], ['²√x', 'botaoraiz', squareroot], ['-', 'botaomenos', minus]],
[['3', 'botao3', three], ['4', 'botao4', four], ['5', 'botao5', five], [';', 'botaopontovirgula', semi], ['+', 'botaomais', plus]],
[['0', 'botao0', zero], ['1', 'botao1', one], ['2', 'botao2', two], ['shift', 'botaoshift', shift], ['=', 'botaoigual', equal]]]

for i in range (0, len(keys)):
    for j in range (0, len(keys[0])):
        exec(f"""{keys[i][j][1]}=tk.Button(master=frm_keys, text=keys[i][j][0], height=1, width=6, font='Calibre 19',
        bg=teclas, borderwidth=0, fg='white', activebackground=teclas2, activeforeground='white', command=keys[i][j][2])""")
        if keys[i][j][0] in '1234567890↊↋':
            exec(f"""{keys[i][j][1]}.config(bg=teclas2, activebackground=teclas2act, activeforeground='white')""")
        if keys[i][j][0]=='=':
            exec(f"""{keys[i][j][1]}.config(bg=corigual, fg='black', activebackground=corigualact, activeforeground=corsimbigual)""")
        exec(f"""{keys[i][j][1]}.grid(row=i, column=j, padx=1, pady=1)""")



janelahistorico=tk.Text(master=window, width=35, height=12, font='Calibre 19', bg=teclas, fg='white')
window.mainloop()
