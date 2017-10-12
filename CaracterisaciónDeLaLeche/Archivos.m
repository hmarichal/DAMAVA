%levantar archivos 
FileName = 'T27_2x1x05.txt';
FileNameS = 'C2_27.csv';

%FileName = 'T27_2x1x05.txt'
data = levantarDatos(FileName);

a = data(:,[5,6,1]);
a(:,2) = -a(:,2);

f = fopen(FileNameS,'w');
fprintf(f,'%d\n',99);
for i=1:99
fprintf(f,' %d %d %d\n',a(i,1),a(i,2),a(i,3));
end
fclose(f);

