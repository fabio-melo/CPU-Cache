# ---------------------------------------------------#
#  Funções do Assembly e Verificação de Tipos        #
# ---------------------------------------------------#

def verify(thing):
    if thing.isdigit(): return 'NUM'
    elif thing.startswith('$'): return 'REG'
    else: return 'MEM'


def inc(dest,memory,register):
    data_dest = verify(dest)
    if   data_dest == 'MEM': memory[dest] += 1
    elif data_dest == 'REG': register[dest] += 1
    else: raise Exception("Operação Inválida")


def dec(dest,memory,register):
    data_dest = verify(dest)
    if   data_dest == 'MEM': memory[dest] -= 1
    elif data_dest == 'REG': register[dest] -= 1
    else: raise Exception("Operação Inválida")


def ldr(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if data_src == 'NUM' and data_dest == 'REG': register[dest] = int(src)
    elif data_src == 'REG' and data_dest == 'REG': register[dest] = register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] = memory[src]
    else: raise Exception("Operação Inválida")

def store(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if data_src == 'NUM' and data_dest == 'MEM': memory[dest] = int(src)    
    if data_src == 'REG' and data_dest == 'MEM': memory[dest] = register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] = register[src]
    else: raise Exception("Operação Inválida")


def mov(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] = int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] = int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] = register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] = register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] = memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


def add(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] += int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] += int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] += register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] += register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] += memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


def sub(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] -= int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] -= int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] -= register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] -= register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] -= memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


def mul(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] *= int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] *= int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] *= register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] *= register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] *= memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


def div(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] /= int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] /= int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] /= register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] /= register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] /= memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


def mod(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    if   data_src == 'NUM' and data_dest == 'MEM': memory[dest] %= int(src)
    elif data_src == 'NUM' and data_dest == 'REG': register[dest] %= int(src)
    elif data_src == 'REG' and data_dest == 'MEM': memory[dest] %= register[src]
    elif data_src == 'REG' and data_dest == 'REG': register[dest] %= register[src]
    elif data_src == 'MEM' and data_dest == 'REG': register[dest] %= memory[src]
    elif data_src == 'MEM' and data_dest == 'MEM': raise Exception("Operações Memória/Memória não são permitidas")
    else: raise Exception("Operação Inválida")


# ---------------------------------------------------#
#  Função Comparação                                 #
# ---------------------------------------------------#


def comp(dest,src,memory,register):
    data_src,data_dest = verify(src),verify(dest)
    flag_test = 0

    if   data_src == 'NUM' and data_dest == 'MEM': flag_test = memory[dest] - int(src)
    elif data_src == 'NUM' and data_dest == 'REG': flag_test = register[dest] - int(src)
    elif data_src == 'REG' and data_dest == 'MEM': flag_test = memory[dest] - register[src]
    elif data_src == 'REG' and data_dest == 'REG': flag_test = register[dest] - register[src]
    else: raise Exception("Operação Inválida")
    
    if flag_test == 0: register['FLAGS'] = 1 # IGUAL
    elif flag_test < 0: register['FLAGS'] = 2 # menor
    elif flag_test > 0: register['FLAGS'] = 3 # maior
    #valor zero
    if data_src == 'NUM' and data_dest == 'MEM' and int(src) == 0: 
        if memory[dest] == 0: register['FLAGS'] = 0
    if data_src == 'NUM' and data_dest == 'REG' and int(src) == 0: 
        if register[dest] == 0: register['FLAGS'] = 0

