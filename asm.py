'''
Projeto de Arquitetura II - Alunos: Fábio Melo e Amarildo Pereira

Funções inspiradas nas encontradas na arquitetura X86 usando a síntaxe Intel (Operation, destination, source)

'''
from sys import argv
import cache as c
import microcode as op
import data as d


# ---------------------------------------------------#
#  Loop de Execução do Programa                      #
# ---------------------------------------------------#


def execute(program,memory,label,min_blocks=2, max_blocks=10, block_inc=1, verbose=False, demo=False, cachesize=4,stress=False,algo="FIFO"):
    
    PC = 0 # Program Counter
    Clock = 0

    register = d.init_reg()
    cache = c.Cache()

    while PC < len(program):

        instruction = program[PC] #fetch da instrução
        cache.caching(instruction)
        if verbose: print("Executando instrução da linha " + str(PC), end=' '); print(instruction)


        # Gerenciamento de Memória

        if   instruction[0] == 'LDR': op.ldr(instruction[1],instruction[2],memory,register) # Load
        elif instruction[0] == 'STR': op.store(instruction[1],instruction[2],memory,register) # Store
        elif instruction[0] == 'MOV': op.mov(instruction[1],instruction[2],memory,register) # Move (Propósito Geral)

        # Incrementar e Decrementar

        elif instruction[0] == 'INC': op.inc(instruction[1],memory,register)
        elif instruction[0] == 'DEC': op.dec(instruction[1],memory,register)

        # Aritimética Simples
        elif instruction[0] == 'ADD': op.add(instruction[1],instruction[2],memory,register)
        elif instruction[0] == 'SUB': op.sub(instruction[1],instruction[2],memory,register)
        elif instruction[0] == 'MUL': op.mul(instruction[1],instruction[2],memory,register)
        elif instruction[0] == 'DIV': op.div(instruction[1],instruction[2],memory,register)
        elif instruction[0] == 'MOD': op.mod(instruction[1],instruction[2],memory,register)

        # Pulo Incondicional
        elif instruction[0] == 'JMP': PC = label.get(instruction[1])
        
        # Comparação
        elif instruction[0] == 'CMP': op.comp(instruction[1],instruction[2],memory,register)
         
        # Pulo Condicional
        elif instruction[0] == 'JZ': #PULO SE ZERO
            if register['FLAGS'] == 0: PC = label.get(instruction[1])
        elif instruction[0] == 'JE': #PULO SE IGUAL
            if register['FLAGS'] == 1: PC = label.get(instruction[1])   
        elif instruction[0] == 'JL': #PULO SE MENOR
            if register['FLAGS'] == 2: PC = label.get(instruction[1])
        elif instruction[0] == 'JG': #PULO SE MAIOR
            if register['FLAGS'] == 3: PC = label.get(instruction[1])

        # para debugging
        elif instruction[0] == "CLEAR": register = d.init_reg() #limpa os registradores

        if verbose: print(memory, end=' '); print(register)
        PC += 1
        Clock += 1
  
    print("Clock Total do Programa: " + str(Clock))
    
    if demo:
        cache.size = cachesize
        if algo == "FIFO": cache.FIFO(verbose=True)
        elif algo == "LRU": cache.LRU(verbose=True)
        elif algo == "OTM": cache.OTM(verbose=True)

    if stress: cache.stress_test(min_blocks, max_blocks, block_inc)
    d.save(memory)


# -------------------------------------------------------------#
#  Código de Rotina do Programa e Leitura de Argumentos        #
# -------------------------------------------------------------#
#  Uso: asm.py (nomedoarquivo), se em branco, usa program.txt  #
#  asm.py --reset recria o arquivo de memória
# -------------------------------------------------------------#


if __name__ == "__main__":
    if len(argv) == 4 and argv[1] == "--demo":
        print("Snapshot de uma Cache de tamanho "+ str(argv[3]))
        program, memory, label = d.generate_sequential_program()
        psize = int(argv[3]); alg = argv[2]
        execute(program,memory,label, 1, 128, demo=True,cachesize=psize,algo=alg)
        exit()

    if len(argv) == 2:
        if argv[1] == "--reset":
            memory = d.init_mem()
            d.save(memory)
            print("Memória Padrão (MEMORY.TXT) Resetada")
            exit()
        elif argv[1] == "--random":
            program, memory, label = d.generate_random_program(program_size=200,memory_size=150, loops=3)
            print("Tamanho do Programa Gerado (em Linhas): " + str(len(program)))
        elif argv[1] == "--seq":
            program, memory, label = d.generate_sequential_program(pseudoprocesses=20, max_pseudoinstructions=20, internalloop=32, loops=1)
            print("Tamanho do Programa Gerado (em Linhas): " + str(len(program)))

        else: 
            program, label = d.load_program(argv[1])
            memory = d.load_memory()
    else: 
        program, label = d.load_program()
        memory = d.load_memory()
    d.printProgram(program)
    d.printMemory(memory)
    execute(program,memory,label, 1, 128, stress=True)        

