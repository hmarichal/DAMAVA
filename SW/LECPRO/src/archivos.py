# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:28:01 2017

@author: henry
"""
import fileinput

def buscar(fileName,stringInput):
    with open(fileName, 'r') as input_file:
        for line in input_file:
            if line.strip() == stringInput:
                return 1
    return 0

    
def reemplazar(fileNameInput,stringInput,stringOutput):
    fileNameOutput = 'archivoAuxiliar.txt'
    with open(fileNameInput, 'r') as input_file, open(fileNameOutput, 'w') as output_file:
        for line in input_file:
            if line.strip() == stringInput:
                output_file.write(stringOutput)
                remplazado = True
                return 1
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
            
    
