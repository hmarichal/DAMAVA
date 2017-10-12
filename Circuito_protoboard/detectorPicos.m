% inicializar variables

f = 10000;
w = 2*pi*f;
to = pi/(2*w);
t = to+1/(10*w):1/(10*w):2*2*pi/w;
C = 1*10^(-6);
R = 10^(4);
T = C*R;
E = 7;
Id = 100*10^(-9);
vco = E*sin(w*to);
vin = E*sin(w*t)
% =====================================

%ic = C*V*0.5*(w/(1+(T*w)^2)*exp(-t/T)+w/(sqrt(1+(T*w)^2))*sin(w*t-atan(T*w)));
%i = vin/(2*R);
%id = ic+i;
io = C*(E*0.5*(-w*exp(-t/T)/(1+(T*w)^2)+(w/(sqrt(1+(T*w)^2)))*cos(w*t-atan(T*w)))-(E/T)*exp(-t/T))+(E*0.5/R)*sin(w*t);
hold on
plot(t*1000,-io*1000,'r',t,zeros(1,length(t)),'k')

xlabel('tiempo(ms)')
ylabel('ID1(mA)')
hold off

vc = E/2*(T*w*exp(-t/T)/(1+(T*w)^2)+sin(t*w-atan(T*w))/sqrt(1+(T*w)^2))+E*exp(-t/T);
figure
plot(t,vc,'b',t,vin/2,'k')

k = find(io>0)