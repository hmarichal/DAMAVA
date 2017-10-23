function data = levantarDatos(FileName)
f = fopen(FileName,'r');
for i=1:4
    lin = fgets(f);
end
points = lin(16:18);

for i=1:4
    lin = fgets(f);
end
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
fclose(f)
end