function [R1,C1,R2,C2,Rm,C3] = AjusteAdmitancia(datos,f)
  
    funDiff = @(x,s)((x(5)*x(3)*x(4)*x(1)*x(2).*s.^2+(x(5)*x(3)*x(4)+x(1)*x(2)*(x(5)+x(3))+x(1)*x(3)*x(4)).*s+x(5)+x(3)+x(1))./...
        (x(1)*x(2)*x(3)*x(4).*s.^2+(x(1)*x(2)+x(3)*x(4)).*s+1) ) 
    funIgual = @(x,s)((x(3)*x(1)*x(2)*x(1)*x(2).*s.^2+(x(3)*x(1)*x(2)+x(1)*x(2)*(x(3)+x(1))+x(1)*x(1)*x(2)).*s+x(3)+x(1)+x(1))./...
        (x(1)*x(2)*x(1)*x(2).*s.^2+(x(1)*x(2)+x(1)*x(2)).*s+1) ) 
    funTodo = @(x,s)((x(5)*x(3)*x(4)*x(1)*x(2).*s.^2+(x(5)*x(3)*x(4)+x(1)*x(2)*(x(5)+x(3))+x(1)*x(3)*x(4)).*s+x(5)+x(3)+x(1))./...
        (x(5)*x(3)*x(4)*x(1)*x(2)*x(6).*s.^3+(x(1)*x(2)*x(3)*x(4)+x(6)*(x(1)*x(4)*x(3)+x(5)*x(3)*x(4)+x(1)*x(2)*x(5)*x(3))).*s.^2+...
        (x(1)*x(2)+x(3)*x(4)+x(5)*x(3)*x(6)).*s+1) )
    x0 = [126,2*10^(-6),805,2*10^(-5),170,0.0001*10^(-9)];
    
    x = lsqcurvefit(funTodo,x0,f,datos);
    figure(1);
    ydata = funTodo(x,f)
    semilogx(imag(f),imag(ydata),'k-',imag(f),imag(datos),'b-');
    legend('Curva ajustada','Curva real')
    title('Reactancia');
    grid minor
    
    figure(2);
    semilogx(imag(f),real(ydata),'k-',imag(f),real(datos),'b-');
    legend('Curva ajustada','Curva real')
    title('Resistencia');
    grid minor
    
    R1 = abs(x(1))
    C1 = abs(x(2))
    R2 = abs(x(3))
    C2 = abs(x(4))
    Rm = abs(x(5))
    C3 = abs(x(6))

    
end