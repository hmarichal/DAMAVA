# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:28:01 2017

@author: henry
"""
import fileinput
    
def reemplazar(fileNameInput,fileNameOutput,stringInput,stringOutput):
    with open(fileNameInput, 'r') as input_file, open(fileNameOutput, 'w') as output_file:
        for line in input_file:
            if line.strip() == stringInput:
                output_file.write(stringOutput)
                return 1
            else:
                output_file.write(line)
    return 0
    
def copiar(fileNameInput,fileNameOutput):    
    with open(fileNameOutput, 'w') as input_file, open(fileNameInput, 'r') as output_file:
        for line in output_file:
            input_file.writelines(line)
            
    
