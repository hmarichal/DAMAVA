close all
clear all
n =9 %cantidad de archivos creados
j =0
nombre ={'N0_C15208_OM14_3.txt','N1_C15289_OM14_3.txt','N2_C12229_OM14_3.txt','N3_C13214_OM14_3.txt','N4_C15090_OM14_3.txt','N5_C15236_OM14_3.txt','N6_C15335_OM14_3.txt','N7_C13322_OM14_3.txt','N8_C14024_OM14_3.txt','N9_C03828_OM14_3.txt','N10_C15100_OM14_3.txt','N11_C14504_OM14_3.txt','N12_C15139_OM14_3.txt'};
nombre = char(nombre);
d=fdesign.lowpass('Fp,Fst,Ap,Ast',0.1,0.25,1,60);
Hd = design(d,'equiripple');

for i= 1:13
   
    filename = nombre(i,:);%['Vaca_UM1_',int2str(i),'.txt']
    datos = load(filename);
    fig = figure
    subplot(3,1,1)
    hold on
    plot(datos(:,1),'r')

    plot(datos(:,2),'b')

    plot(datos(:,3),'g')

    plot(datos(:,4),'k')
    legend('1 ','2 ' ,'3 ','4 ')
    hold off
    output = filter(Hd,datos(:,5));
    subplot(3,1,3)
    plot(output,'r')
    axis([20 350 20 40])
    subplot(3,1,2)
    plot(datos(:,5),'r')
    direc =['GRAFICAS\',filename(1:end-5),'.png']
    print(fig,direc,'-dpng')
    close all;
end
