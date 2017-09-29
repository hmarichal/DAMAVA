close all
fun0 = @(x,xdata)-atan(1./(x(1)*x(2)*2*pi*xdata));
r = 1:1:1000;
c = linspace(1,10^15);
c = c*10^-30;

[X,Y] = meshgrid(r,c);
x = X(:);
y = Y(:);
dist = [];

for i=1:1000
ydata = fun0([x(i),y(i)],freq(1:51));
dist = [dist,abs(norm(ydata-fase(1:51)))];

end

[v,i] = min(dist);
xo = [x(i),y(i)];
figure;
ydata = fun0(xo,freq(1:51));
semilogx(freq(1:51),ydata,'k-',freq(1:51),fase(1:51),'b-');
legend('Curva ajustada','Curva real')
title('Fase');
grid minor

[R,C] = lsqcurvefit(fun0,xo,freq(1:51),fase(1:51));
figure;
ydata = fun0([R,C],freq(1:51));
semilogx(freq(1:51),ydata,'r-',freq(1:51),fase(1:51),'b-');
legend('Curva ajustada','Curva real')
title('Fase');
grid minor
