import json, os, random
import tkinter as tk

# ---------------------------------------------------#
#  Inicialização e Leitura de Arquivos               #
# ---------------------------------------------------#


def load_program(program_file="default.asm"):
    
    program, label = [],{} # Program 

    with open(program_file,'r') as progfile:
        x = 0
        for line in progfile: 
            code = line.rstrip().split(" ")
            if len(code) == 1 and code[0].endswith(":"): 
                label[code[0][:-1]] = x 
            program.append(code)
            x += 1

    return program, label

def load_memory(memory_file="memory.txt"):
    memory = json.load(open(memory_file,"r"))
    return memory

def save(memory, memory_file="MEMORY.TXT"):
    json.dump(memory, open(memory_file,"w"))

def init_reg():
    register = {"$R1": 0, "$R2": 0, "$R3": 0, "$R4": 0, "FLAGS": -1}
    return register

def init_mem(size=10):
    memory = {}
    for x in range(1,size+1):
        memory["M"+str(x)] = 0
    return memory

def generate_random_memory(size, max_number=9999):
    memory = {}
    for x in range(1,size+1):
        memory["M"+str(x)] = random.randint(0, max_number)
    return memory    

def generate_random_program(program_size=200, memory_size=1000, loops=5, max_number=9999):
    memory = generate_random_memory(memory_size)
    program, label = [], {}
    operations = ["ADD","SUB","MUL","EXP","MOV"]
    line1 = ["START:"]
    line2 = ["MOV", "$R1", str(loops)]
    line3 = ["LOOP:"]
    program.append(line1);program.append(line2);program.append(line3)

    for x in range(program_size):
        line4 = [random.choice(operations), str("M" + str(random.randint(1,memory_size))), str(random.randint(0,max_number))]
        line5 = [random.choice(operations), "$R2", str("M" + str(random.randint(1,memory_size)))]
        line6 = [random.choice(operations), str("M" + str(random.randint(1,memory_size))), "$R2"]
        program.append(line4);program.append(line5);program.append(line6)

    line7 = ["DEC", "$R1"]
    line8 = ["CMP", "$R1", "0"]
    line9 = ["JZ", "END"]
    line10 = ["JMP", "LOOP"]
    line11 = ["END:"]
    program.append(line7);program.append(line8);program.append(line9);program.append(line10);program.append(line11)

    label["START"] = 0; label["LOOP"] = 3; label["END"] = len(program)-1
    
    return program, memory, label

def generate_sequential_program(pseudoprocesses=20, max_pseudoinstructions=10, memory_size=1000, loops=1, internalloop=4, max_number=9999):
    memory = generate_random_memory(memory_size)
    program, label = [], {}

    operations = ["ADD","SUB","MUL","EXP","MOV"]
    line1 = ["START:"]
    line2 = ["MOV", "$R4", str(loops)]
    line3 = ["LOOP:"]
    program.append(line1);program.append(line2);program.append(line3)

    for x in range (pseudoprocesses):
        process_id = random.randint(0,memory_size)
        label["PROCESS"+ str(x)] = len(program)-1

        max_process_size = min(memory_size - process_id, max_pseudoinstructions)
        line4 = ["PROCESS"+ str(x) + ":"]
        program.append(line4)

        for y in range (random.randint(1,internalloop)):
            for z in range (random.randint(1,max_process_size)):
                if (process_id+z) <= memory_size:
                    line5 = [random.choice(operations), "M" + str(process_id+z), str(random.randint(0,max_number))]
                    program.append(line5)

    line7 = ["DEC", "$R4"]
    line8 = ["CMP", "$R4", "0"]
    line9 = ["JZ", "END"]
    line10 = ["JMP", "LOOP"]
    line11 = ["END:"]
    program.append(line7);program.append(line8);program.append(line9);program.append(line10);program.append(line11)

    label["START"] = 0; label["LOOP"] = 3; label["END"] = len(program)-1

    return program, memory, label            
            








# ---------------------------------------------------#
#  Operações de Benchmarking do Clock                #
# ---------------------------------------------------#

def update_clock():
    with open("clock.tmp",'a') as clock:
        clock.write("i")

def print_clock():
    with open("clock.tmp",'r') as clockfile:
        clock = clockfile.read()
        print("Total de Ciclos do Clock: " + str(len(clock)))
    if os.path.exists("clock.tmp"):
        os.remove("clock.tmp")

def printProgram(program):

    root = tk.Tk()
    root.title("Programa")
    root.geometry("200x800+70+0")
    text = tk.Text(root, font="Consolas",background="#151929",fg="white")
    for line in program:
        text.insert(tk.INSERT, line)
        text.insert(tk.INSERT, "\n")
    text.pack(fill="both", expand=True)

    text.tag_add("here", "1.0", "1.4")
    text.tag_add("start", "1.8", "1.13")

def printMemory(mem):

    root = tk.Tk()
    root.title("Memoria")
    root.geometry("800x200+250+500")
    text = tk.Text(root, font=("Consolas",10),background="#424C77",fg="white")
    text.insert(tk.INSERT, mem)
    text.pack(fill="both", expand=True)

    text.tag_add("here", "1.0", "1.4")
    text.tag_add("start", "1.8", "1.13")

