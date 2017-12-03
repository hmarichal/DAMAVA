# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:28:01 2017

@author: henry
"""
import fileinput
#            print line
#            if salir == 1:
#                return line[:-1]

def buscar(fileName,stringInput):
    salir = 0
    with open(fileName, 'r') as input_file:
        for line in input_file:
            if salir == 1:
                return line[:-1]
            if line == stringInput:
                salir = 1
    return int(0)

    
def reemplazar(fileNameInput,stringInput,stringOutput):
    fileNameOutput = 'archivoAuxiliar.txt'
    siguiente,remplazado = False,False
    with open(fileNameInput, 'r') as input_file, open(fileNameOutput, 'w') as output_file:
        for line in input_file:
            if siguiente:
		   siguiente = False
		   continue
            if line == stringInput:
                output_file.write(stringOutput)
                remplazado = True
                siguiente = True
            else:
                output_file.write(line)
    if remplazado:
        copiar(fileNameOutput,fileNameInput)
        return 1
    else:
        return 0

def copiar(fileNameInput,fileNameOutput):
    with open(fileNameOutput, 'w') as input_file, open(fileNameInput, 'r') as output_file:
        for line in output_file:
            input_file.writelines(line)
            
    
