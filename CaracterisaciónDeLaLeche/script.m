close all
clear all

FileName = 'T33_1x1x1.txt';
%FileName = 'T27_2x1x05.txt'
data = levantarDatos(FileName);


% frequency impedance admittance phase-angle resistence reactance
% conductance suceptance

n = 99;

x = fliplr(data(:,5)');
y = fliplr(data(:,6)');
freq = fliplr(data(:,1)');

rango =[1:70];
[R1,C1,R2,C2,Rm,C3] = AjusteAdmitancia(x(rango)+j*y(rango),2*pi*freq(rango)*j);


