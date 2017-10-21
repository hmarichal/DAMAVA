function z = ModeloEquivalente(x,s)

z1 = x(1)./(x(1)*x(2)*s+1);
z2 = x(3)./(x(3)*x(4)*s+1);
zarr = z2+z1+x(5);
z = zarr./(zarr.*x(6).*s+1);


end