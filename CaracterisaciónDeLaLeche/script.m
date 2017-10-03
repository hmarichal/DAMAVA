close all
FileName = 'T27_2x1x05.txt';
f = fopen(FileName,'r');
for i=1:4
    lin = fgets(f);
end
points = lin(16:18);

for i=1:4
    lin = fgets(f);
end
% frequency impedance admittance phase-angle resistence reactance
% conductance suceptance
format = '%e';
ind = 1;

data = [];
points = str2num(points);
sizeA = [1];
while (ind<=points)
    A = [];
    for i=1:8
        b = fscanf(f,format,1);
        A = [A,b];
    end    
    data = [data;A];
    ind = ind+1;
end
n = 99;
figure(5)
freq = fliplr(data(:,1)');
conductancia = fliplr(data(:,7)');
suceptancia = fliplr(data(:,8)');
[hAx,hLine1,hLine2] = plotyy(log10(freq(1:n)),1000*conductancia(1:n),log10(freq(1:n)),1000*suceptancia(1:n));
title('Dependencia de la frecuencia de la Conductancia y la Suceptancia')
xlabel('Log f(Hz)')
ylabel(hAx(1),'Conductancia (mS)')
ylabel(hAx(2),'Suceptancia (mS)')

figure(4)
plot(log10(freq))


figure(1)
subplot(2,1,1)
title('Bode')
semilogx(data(:,1),data(:,7),'ro')
hold on
semilogx(data(:,1),data(:,8),'bx')
hold off
xlabel('frecuencia (Hz)')
ylabel('resitencia(ohm)')
grid minor 

subplot(2,1,2)
semilogx(data(:,1),data(:,4))
xlabel('frecuencia (Hz)')
ylabel('fase(grados)')
grid minor

figure
freq = fliplr(data(:,1)');
fase = fliplr(data(:,4)');
semilogy(2*pi*freq);
%[R,Cpm,Cpp] = AjusteFase(fase,freq);
%display('Resistencia');
%display(R);
%display('Cpm');
%display(Cpm);
%display('Cpp');
%display(Cpp);
fclose(f)
 
    








%fclose(f)