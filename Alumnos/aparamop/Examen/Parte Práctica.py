import numpy as np 

def rosen(x):
    a = 1
    b = 100
    resultado = (a - (x[0]))**2 + b*((x[1]) - ((x[0])**2))**2
    return resultado  

def alg_newton(f, x0): 
    """
    Algoritmo de búsqueda lineal con dirección de Newton
    """
    xk = x0
    while not (f_o_c(f,xk) and s_o_c(f,xk)):
        grad = Grad(f,xk)
        hess = Hess(f,xk)
        pk = np.linalg.solve(hess, -grad)
        xk = xk + pk

    return xk     

def alg_busq_lineal(f, x0): 
    """
    Algoritmo de búsqueda lineal con dirección de Newton
    """
    xk = x0
    while not (f_o_c(f,xk) and s_o_c(f,xk)):
            grad = Grad(f,xk)
            pk = -grad
            alpha = genera_alpha(f, xk, pk)
            xk = xk + alpha*pk
    return xk

def Grad(f, x0, h=1e-6, i=-1):
    """
    Función que calcula el Grad de una función en un punto
    """
    n = len(x0)
    if i in range(n):
        z = np.zeros(n)
        z[i] = h/2
        Grad = (f(x0 + z) - f(x0 - z))/h
    else:
        Grad = np.zeros(n)
        for j in range(n):
            z = np.zeros(n)
            z[j] = h/2
            Grad[j]= (f(x0 + z) - f(x0 - z))/h
    return Grad

def Hess(f, x0, h=1e-4, method = "basic"):
    """
    Función que calcula la Hessiana  de una función en un punto. 
    f: función sobre la cual queremos calcular la hessiana.
    x0: Punto sobre el cual queremos hacer el cálculo
    h: nivel de precisión para hacer el cálculo
    method: Método por el cual se quiere hacer puede ser: 'basic', 'grad', 'centered', 'gradCentered'
    """
    n = len(x0)
    Hess = np.matrix(np.zeros((n,n)))
    for i in range(n):
        for j in range(n):
            z_i = np.zeros(n)
            z_j = np.zeros(n)
            if j<= i :
                z_i[i] = h
                z_j[j] = h
                if method == "basic":
                    Hess[i,j] = ( f(x0 + z_j +z_i) - f(x0 + z_i ) - f(x0+z_j) +f(x0)) / (h**2)
                    Hess[j,i] = Hess[i,j]
                elif method == "grad":
                    Hess[i,j] = (Grad(f,x0+z_j,h,i) - Grad(f,x0,h,i) + \
                                Grad(f,x0+z_i,h,j) - Grad(f,x0,h,j))/(2*h)
                    Hess[j,i] = Hess[i,j]
                elif method == "centered":
                    if i==j:
                        Hess[i,j] = (-f(x0+2*z_i) + 16*f(x0+z_i) - 30*f(x0)+\
                                    16*f(x0-z_i) - f(x0-2*z_i))  / (12*h**2)
                        Hess[j,i] = Hess[i,j]
                    else :
                        Hess[i,j] = (f(x0+z_i+z_j) - f(x0 + z_i - z_j) - \
                                    f(x0 - z_i + z_j) + f(x0-z_i-z_j))/(4*h**2)
                        Hess[j,i] = Hess[i,j]
                elif method == "gradCentered":
                        Hess[i,j] = (Grad(f,x0+z_j,h)[i] - Grad(f, x0-z_j,h)[i] + \
                                    Grad(f,x0+z_i,h)[j] - Grad(f,x0-z_i,h)[j])/(4*h)
                        Hess[j,i] = Hess[i,j]
    return Hess


def f_o_c(f, x0, tol=1e-12):
    """
    Función que calcula las condiciones de primer orden
    """
    grad = np.array(Grad(f, x0))
    if np.dot(grad, grad) < tol:
        return True
    else :
        return False


def s_o_c(f, x0, tol=1e-15):
 
    hess = Hess(f, x0, tol)
    print(np.linalg.eigvals(hess))
    if np.all(np.linalg.eigvals(hess) > tol) :
        return True
    else :
        return False


def genera_alpha(f, x0, pk, c1=1e-4, tol=1e-5):
    """
    Backtracking LS i.e. Algoritmo que encuentra una alpha que cumpla condiciones de wolfe. 
    """
    alpha, rho, c = 1, 4/5, c1
    while f(x0 + alpha*pk)>f(x0) + c*alpha*np.dot(Grad(f, x0),pk):
        alpha*=rho
    return alpha

"""
def is_pos_def(Hessiana):
    if np.all(np.linalg.eigvals(Hessiana) > 0):
        return True


def modificacion_hessiana(Hessiana, l = 0.5):
    while not is_pos_def(Hessiana):
        Hessiana = Hessiana + l*np.eye(len(Hessiana))
    return Hessiana

"""


import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np



print("Resultado Newton")
print(alg_newton(rosen,[0,0]))
print("")
print("Resultado Búsqueda Lineal")
print(alg_busq_lineal(rosen,[1,1]))

