# LIBS_________________________________________________________________________________________________
import hashlib as h 
from tkinter import Tk, ttk, PhotoImage, filedialog
import pyperclip

# CRIPTOGRAFIAS________________________________________________________________________________________
def sha256(arquivo):
    algoritmo_sha256 = h.sha256()   # Cria um objeto de hash SHA-256
    
    # Abre o arquivo em modo de LEITURA BINÁRIA 
    with open(arquivo, 'rb') as f:
        dados = f.read() # Leitura do arquivo completo
        
    algoritmo_sha256.update(dados)  
    return algoritmo_sha256.hexdigest() # CRIPTOGRAFIA sha-256

def md5(arquivo):
    algoritmo_md5 = h.md5()   # Cria um objeto de hash MD5
    
    # Abre o arquivo em modo de LEITURA BINÁRIA 
    with open(arquivo, 'rb') as f:
        dados = f.read() # Leitura do arquivo completo
    
    algoritmo_md5.update(dados)
    return algoritmo_md5.hexdigest() # CRIPTOGRAFIA md5

# CÁLCULOS DE HASH_____________________________________________________________________________________
def calculaHashArquivo():
    global caminho
    caminho = filedialog.askopenfilename()

    # Verifica se um arquivo foi selecionado
    if caminho:
        # Calcula os valores usando as funções sha256 e md5
        md5_hex = md5(caminho)
        sha256_hex = sha256(caminho)

        # Atualiza os rótulos com os valores calculados
        saidaMD5_HEX.config(text=f'{md5_hex}')
        saidaSHA256_HEX.config(text=f'{sha256_hex}')
        atualizaJanela()
            
    return caminho

def calculaHashArquivoTexto():
    texto = entradaTexto.get() # Pega a entry "entradaTexto"  
    
    if texto:   
        textoCoding = texto.encode('utf-8') # Converte o texto para bytes (UTF-8)
        
        # Criptografa o texto convetido para bytes 
        global h_MD5, h_SHA256
        h_MD5 = h.md5(textoCoding)
        h_SHA256 = h.sha256(textoCoding)
        
        # Atualiza os rótulos com os valores calculados
        saidaMD5_HEX.config(text=f'{h_MD5.hexdigest()}')
        saidaSHA256_HEX.config(text=f'{h_SHA256.hexdigest()}')
        atualizaJanela()
        
    return h_MD5, h_SHA256

# FUNÇÕES PARA CHECAR AUTENTICIDADE DE HASH____________________________________________________________
def check_MD5():
    checkOK = ttk.Label(janela, image=images['check'])
    checkOK.grid(row=5, column=0, pady=10)
    retornoCheck = ttk.Label(janela, text='           MD5 HEXADECIMAL           ', font=("Arial", 15, 'bold'), foreground='green')
    retornoCheck.grid(row=5, column=1, padx=3, pady=5)  
    atualizaJanela()

def check_SHA256():
    checkOK = ttk.Label(janela, image=images['check'])
    checkOK.grid(row=5, column=0, pady=10)
    retornoCheck = ttk.Label(janela, text='           SHA-256 HEXADECIMAL           ', font=("Arial", 15, 'bold'), foreground='green')
    retornoCheck.grid(row=5, column=1, padx=3, pady=5)  
    atualizaJanela()
    
def NOcheck():
    noCheck = ttk.Label(janela, image=images['no_check'])
    noCheck.grid(row=5, column=0, pady=10)
    retornoCheck = ttk.Label(janela, text='NÃO CORREESPONDENTE', font=("Arial", 15, 'bold'), foreground='red')
    retornoCheck.grid(row=5, column=1, padx=3, pady=5)   
    atualizaJanela()

def checking():  
    verificaCheck = entryCheck.get()
    
    # Autenticidade de hash para arquivos
    if 'caminho' in globals():
        md5_hex = md5(caminho)
        sha256_hex = sha256(caminho)
        
        if verificaCheck == md5_hex:  check_MD5()          
        elif verificaCheck == sha256_hex: check_SHA256()         
        else: NOcheck()
    
    # Autenticidade de hash para textos
    else:               
        if verificaCheck == h_MD5.hexdigest(): check_MD5()                                                      
        elif verificaCheck == h_SHA256.hexdigest(): check_SHA256()                           
        else: NOcheck()

def atualizaJanela():
    janela.update_idletasks()
    janela.geometry(f'{janela.winfo_reqwidth()}x{janela.winfo_reqheight()}')        

#######################################################################################################
# Configuração da janela ttkINTER
janela = Tk()
janela.title("SHA256&MD5 CODDING")
janela.configure(bg='#001F3F') # Azul Escuro = #001F3F 
janela.geometry('700x250')
janela.iconbitmap('cripto.ico')

# Estilo para os BOTÕES
style = ttk.Style()
style.configure('TButton', font=("Arial", 15, 'bold'))

# Configuração do plano de fundo dos Labels
style.configure('TLabel', background='#001F3F')

# Carrega arquivo
botao_selecionar = ttk.Button(janela, text="        CARREGAR ARQUIVO        ", style='TButton', command=calculaHashArquivo)
botao_selecionar.grid(row=0, column=1, pady=10)

# Entrada de Texto
criptografaTexto = ttk.Button(janela, text="TEXTO", style='TButton', command=calculaHashArquivoTexto)
criptografaTexto.grid(row=1, column=0, padx=3, pady=10)
entradaTexto = ttk.Entry(janela, width=40, font=("Arial", 17, 'bold'))
entradaTexto.grid(row=1, column=1, padx=3, pady=5, ipady=5)

# SAÍDA MD5
labelMD5_HEX = ttk.Label(janela, text='MD5 (hex):', font=("Arial", 15, 'bold'), foreground='black')
labelMD5_HEX.grid(row=2, column=0, padx=3, pady=5)
saidaMD5_HEX = ttk.Label(janela, text='', font=("Arial", 17, 'bold'), foreground='black')
saidaMD5_HEX.grid(row=2, column=1, padx=3, pady=5)
saidaMD5_HEX.bind("<Button-1>", lambda e: pyperclip.copy(saidaMD5_HEX.cget("text")))

# SAÍDA SHA-256
labelSHA256_HEX = ttk.Label(janela, text='SHA-256 (hex):', font=("Arial", 15, 'bold'), foreground='black')
labelSHA256_HEX.grid(row=3, column=0, padx=3, pady=5)
saidaSHA256_HEX = ttk.Label(janela, text='', font=("Arial", 17, 'bold'), foreground='black')
saidaSHA256_HEX.grid(row=3, column=1, padx=3, pady=5)
saidaSHA256_HEX.bind("<Button-1>", lambda e: pyperclip.copy(saidaSHA256_HEX.cget("text")))

# Conferência da CRIPTOGRAFIA
buttonCheck = ttk.Button(janela, text="CHECK", style='TButton', command=checking)
buttonCheck.grid(row=4, column=0, padx=3, pady=10)
entryCheck = ttk.Entry(janela, width=40, font=("Arial", 17, 'bold'))
entryCheck.grid(row=4, column=1, padx=3, pady=5, ipady=5)

# IMAGENS CHECK & NOCHECK
images = {'check': None, 'no_check': None} # Dicionário com valores nulos para armazenar imagens
images['check'] = PhotoImage(file='check.png')
images['check'] = images['check'].subsample(8, 8)  # Reduz o tamanho para 15x15 pixels
images['no_check'] = PhotoImage(file='noCheck.png')
images['no_check'] = images['no_check'].subsample(8, 8)  # Reduz o tamanho para 15x15 pixels

janela.mainloop() # Executa o loop da janela

'''
print('• Algoritmos disponíveis')
print(h.algorithms_available)
print('')
print('• Algoritmos disponíveis NO WINDOWS')
print(h.algorithms_guaranteed)
print('')
'''
