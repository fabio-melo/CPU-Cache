import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

class Cache:
    def __init__(self, size=3):
       self.size = size
       self.cachelist = []
       self.FIFO_hits, LRU_hits, OTM_hits = 0, 0, 0
       self.FIFO_faults, self.LRU_faults, self.OTM_faults = 0, 0, 0

    def is_memory(self, pos):
        if isinstance(pos,int): return False
        elif pos.startswith('M'): return True
        else: return False

    def caching(self, instruction):
        if len(instruction) == 2 and self.is_memory(instruction[1]):
            self.cachelist.append(instruction[1])
        elif len(instruction) == 3:
            if self.is_memory(instruction[1]): self.cachelist.append(instruction[1])
            if self.is_memory(instruction[2]): self.cachelist.append(instruction[2])

    def printcachelist(self):
        print(self.cachelist)

    def FIFO(self,verbose=False):
        block = [None for x in range(self.size)] #prealoca o tamanho da bloco 
        pos = 0 #posição na bloco
        fault, hit = 0, 0
        for x in self.cachelist:
            if x not in block: #se bloco não encontrada
                block[pos % self.size] = x #sobreescreve a posição da primeira pagina colocada, se não vazia.
                pos += 1 #incrementa posição
                fault += 1 #marca falta
            else: hit += 1 #marca hit
            if verbose: print(block)
        
        self.FIFO_faults, self.FIFO_hits = fault, hit

    # Algorítimo Least-Recently-Used (LRU)
    def LRU(self, verbose=False):
        block = []
        fault, hit = 0,0 #qtd de faltas de pagina

        for x in self.cachelist:
            if x not in block and len(block) < self.size: #se a memória não está cheia, coloca a pagina na memória e marca falta
                block.append(x)
                fault += 1
            elif x not in block and len(block) == self.size: #se a memória estiver cheia e faltar bloco, remove a pagina no fundo da stack
                block.append(x)
                block.pop(0)
                fault +=1
            elif x in block: #se a pagina for encontrada, à move para o topo da stack
                block.remove(x)
                block.append(x)
                hit += 1
            if verbose: print(block)
        self.LRU_faults, self.LRU_hits = fault, hit

    # Algoritimo Otimo
    def OTM(self,verbose=False):
        block = []
        pos, fault, hit = 0, 0, 0 #além dos faltas de bloco, guardamos a posição atual do paginador
        
        for x in self.cachelist: #para cada bloco
            if x not in block and len(block) < self.size: #se a memória não estiver cheia, adiciona a bloco e marca a falta.
                block.append(x)
                fault += 1
                pos += 1
            elif x not in block and len(block) == self.size: #se a memória estiver cheia e a pagina não estiver na memória, executa a rotina de substitução
                block.pop(self.OTM_predict(block,self.cachelist,pos)) #remove a pagina com maior distancia futura
                block.append(x) #adiciona a bloco nova
                fault +=1 #marca falta de pagina
                pos += 1 #incrementa posição
            elif x in block:
                pos += 1
                hit += 1 #achou a bloco, HIT, incrementa a posição
            if verbose: print(block)
        self.OTM_faults, self.OTM_hits = fault, hit

        # Função Auxiliar do algoritimo ótimo que verifíca quais blocos serão utilizados no futuro, 
        # e retorna a posição da pagina a ser removida
    def OTM_predict(self, estado, paginas, pos):
        futuro = paginas[pos:] #salva em uma listas as futuras blocos a serem chamados
        indices = [] #cria uma lista para armazenar valores das posições dos blocos

        for x in estado: #para cada bloco atualmente na memória
            try:
                indices.append(futuro.index(x)) #tenta pegar a posição relativa a primeira aparição na lista de blocos futuras 
            except ValueError:
                indices.append(9999999999999) #caso não o ache no futuro, o marca com um valor infinito
        return indices.index(max(indices)) # retorna a posição da pagina com o maior valor, para remoção

    def stress_test(self, min_blocks=2, max_blocks=10,inc=1):
        table = []
        #headers = ["Tamanho da Cache", "Faults(FIFO)", "Faults(LRU)", "Faults(OTM)","Hits(FIFO)","Hits(LRU)", "Hits(OTM)"]
        #table.append(headers)
        for x in range(min_blocks,max_blocks,inc):
            self.size = x
            self.FIFO();self.LRU();self.OTM()
            
            line = [x, self.FIFO_faults, self.LRU_faults, self.OTM_faults, self.FIFO_hits, self.LRU_hits, self.OTM_hits]
            printProgressBar(x, max_blocks)
            table.append(line)
        printTable(table)
        printGraph(table)



# ---------------------------------------------------#
#  Imprimir Tabela Bonitinha                         #
# ---------------------------------------------------#


def printTable (tbl):
   
    root = tk.Tk()
    root.title("Cache")
    root.geometry("800x500")
    tree = ttk.Treeview(root)

    tree["columns"]=("FIFOF","LRUF","OTMF","FIFOH","LRUH","OTMH")
    tree.column("FIFOF", width=100)
    tree.column("LRUF", width=100)
    tree.column("OTMF", width=100)
    tree.heading("FIFOF", text="Faults(FIFO)")
    tree.heading("LRUF", text="Faults(LRU)")
    tree.heading("OTMF", text="Faults(OTM)")

    tree.column("FIFOH", width=100)
    tree.column("LRUH", width=100)
    tree.column("OTMH", width=100)
    tree.heading("FIFOH", text="Hits(FIFO)")
    tree.heading("LRUH", text="Hits(LRU)")
    tree.heading("OTMH", text="Hits(OTM)")


    for x in tbl:
        tree.insert("",x[0], text=x[0], values=(x[1],x[2],x[3],x[4],x[5],x[6]))

    tree.pack(fill="both", expand=True)


def printGraph(table):
    block_t = []
    fifo_f, lru_f, otm_f = [],[],[]
    fifo_h, lru_h, otm_h = [],[],[]
    
    for x in table:
        block_t.append(x[0])
        fifo_f.append(x[1]);lru_f.append(x[2]);otm_f.append(x[3])
        fifo_h.append(x[4]);lru_h.append(x[5]);otm_h.append(x[6])
    
    f, plots = plt.subplots(2, sharex=True)

    plots[0].grid(True)
    plots[1].grid(True)
    plt.xlabel('Tamanho da Cache')
    plt.ylabel('Qtd de Faltas/Acertos')
    plots[0].plot(tuple(block_t),tuple(fifo_f))
    plots[0].plot(tuple(block_t),tuple(lru_f))
    plots[0].plot(tuple(block_t),tuple(otm_f))
    plots[1].plot(tuple(block_t),tuple(fifo_h))
    plots[1].plot(tuple(block_t),tuple(lru_h))
    plots[1].plot(tuple(block_t),tuple(otm_h))
    plots[0].legend(['FIFO', 'LRU', 'OTM'], loc='upper left')
    plots[1].legend(['FIFO', 'LRU', 'OTM'], loc='upper left')
    plots[0].set_title("Falta de Cache (Faults)")
    plots[1].set_title("Acertos em Cache (Hits)")

    plt.show()




def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()
