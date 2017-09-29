function [R,Cpm,Cpp] = AjusteFase(H,f)
    %hasta la muestra 51
    fun0 = @(x,xdata)-atan(1./(x(1)*x(2)*2*pi*xdata));
    x0 = [700,10^(-5)];
    options = optimset('MaxFunEvals',2000,'LB');
    x = lsqcurvefit(fun0,x0,f(1:51),H(1:51),options)
    figure;
    ydata = fun0(x,f(1:51));
    semilogx(f(1:51),ydata,'k-',f(1:51),H(1:51),'b-');
    legend('Curva ajustada','Curva real')
    title('Fase');
    grid minor
    
    %x = [R,Cpm,Cpp]
    fun = @(x,xdata)-atan(((x(1)^(2))*x(2)*((x(2)*x(3))/(x(2)+x(3)))*(2*pi*xdata).^2+1)./(x(1)*(x(2)-((x(2)*x(3))/(x(2)+x(3))))*2*pi*xdata))*180/pi;
    x0 = [700,0.00000701,0.0000000701];
    x = lsqcurvefit(fun,x0,f,H);
    
    R = x(1);
    Cpm = x(2);
    Cpp = x(3);
    figure;
    ydata = fun([R,Cpm,Cpp],f);
    semilogx(f,ydata,'k-',f,H,'b-');
    legend('Curva ajustada','Curva real')
    title('Fase');
    grid minor
end