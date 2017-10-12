close all
clear all

FileName = 'T27_2x1x05.txt';
%FileName = 'T27_2x1x05.txt'
data = levantarDatos(FileName);


% frequency impedance admittance phase-angle resistence reactance
% conductance suceptance

n = 99;

x = fliplr(data(:,5)');
y = fliplr(data(:,6)');
freq = fliplr(data(:,1)');

rango =[1:70];

x133 = [96,2.5*10^(-6),520,1.86*10^-5,145,4.18*10^-11];
x127 = [5080,371*10^(-6),520,7.8*10^-6,145,4.18*10^-11];
x327 = [45,4.17*10^-5,10^6,147*10^-6,86,3*10^-11]
x227 = [772,9.17*10^-6,10^6,147*10^-6,740,3*10^-11];
 
[R1,C1,R2,C2,Rm,C3] = AjusteAdmitancia(x(rango)+j*y(rango),2*pi*freq(rango)*j,x227);


