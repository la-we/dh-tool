from tkinter import *
from tkinter import ttk
from sympy.matrices import Matrix
from sympy.printing.str import StrPrinter
import math

printer = StrPrinter()
entries = []
rows = 0
master = Tk()

matIn = "[1,1,1,1;2,2,2,2;3,3,3,3;4,4,4,4]" #for testing

def multi(mats):
    return mats.pop(0) * multi(mats) if len(mats) >= 1 else 1

def parseStr2Mat(mat): #input matrix formatted as string in 'Matlab-style' => sep = ';'
    mat = mat.strip('[')
    mat = mat.strip(']')
    matOut = []
    for elem in mat.split(';'):
        matOut.append(elem.split(','))
    return Matrix(matOut)

def genA(theta, d, alpha, a): #all inputs as string, will be parsed afterwards
    return parseMat(Matrix([ ['c(' + theta +')', '-s(' + theta +')*c(' + alpha + ')',  's(' + theta +')*s(' + alpha + ')', '' + a + '*c(' + theta + ')'], \
                    ['s(' + theta +')',  'c(' + theta +')*c(' + alpha + ')', '-c(' + theta +')*s(' + alpha + ')', '' + a + '*s(' + theta + ')'], \
                    [                0,                   's(' + alpha +')',                   'c(' + alpha +')',                           d ], \
                    [                0,                                   0,                                   0,                           1 ] ]))

def printMat(mat): #prints a reasonably good string representation of a matrix
    return mat.table(printer)
    

def parseMat(mat):
    strRep = mat.table(printer, rowsep=';', rowstart='', rowend='')
    strRep = strRep.replace('c(0)', '1') 
    strRep = strRep.replace('s(0)', '0')
    #strRep = strRep.replace('s(', 'math.sin(')
    #strRep = strRep.replace('c(', 'math.cos(')
    return Matrix(parseStr2Mat(strRep))

def addrow(f, entries):
    rows = len(entries)
    width = 8
    entries.append([ttk.Entry(f, width=width),\
                     ttk.Entry(f, width=width),\
                     ttk.Entry(f, width=width),\
                     ttk.Entry(f, width=width)])
    i = 0
    for entry in entries[len(entries)-1]:
        entry.grid(column=i,row=rows, sticky=(N,W))
        i += 1
    

def delrow(f, entries):
    for entry in entries[len(entries)-1]:
        entry.destroy()
    entries.pop()

def generate(l):
    value = []; values = []; mats = []
    l.grid(column=0, row=len(entries)+1, sticky=S)
    for entry in entries:
        for var in entry:
            value.append(var.get())
        values.append(value)
        value = []
    for value in values:
        mats.append(genA(value[0],value[1],value[2],value[3]))
    l["text"] = printMat(multi(mats))

content = ttk.Frame(master)
content.grid(column=0, row=0, sticky=(N, W, E ,S))

entryFrame = ttk.Frame(content)
entryFrame.grid(column=0,row=1, sticky=(N,W,S,E))

buttonFrame = ttk.Frame(content)
buttonFrame.grid(column=1,row=1, sticky=(N,W,S,E))

lTableDesc = ttk.Label(content,justify=CENTER, text="Denavit-Hartenberg Tabelle:\n| theta |   d   | alpha |   a   |")
lTableDesc.grid(column=0, row=0, sticky=N)

lOutput = ttk.Label(entryFrame,justify=LEFT, text="")
lOutput.grid(column=0, row=len(entries)+1, sticky=S,columnspan=4)

buttonAddRow = ttk.Button(buttonFrame, text="Add Row", command= lambda: addrow(entryFrame, entries))
buttonAddRow.grid(column=0, row=0, sticky=(N, W))

buttonDelRow = ttk.Button(buttonFrame, text="Del Row", command= lambda: delrow(entryFrame, entries))
buttonDelRow.grid(column=0, row=1, sticky=(N, W))

buttonGenMat= ttk.Button(buttonFrame, text="Generate", command= lambda: generate(lOutput))
buttonGenMat.grid(column=0, row=2, sticky=(N, W))


master.title("Test")
master.mainloop()
