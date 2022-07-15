import math

x, y = 3, -4 #example values

#forward pass
sigy = 1.0/(1+math.exp(-y))#sigmoid function with respect to y    #(1)
num = x+sigy# numerator completed                               #(2)
sigx = 1.0/(1+math.exp(-x))#sigmoid function with respect to x    #(3)
xpy = x+y                                                       #(4)
xpysqr = xpy**2                                                 #(5)
den = sigx + xpysqr #denominator                                #(6)
invden = 1/ den                                                 #(7)
f  = num * invden                                               #(8)

# Backprop f  = num * invden
dnum =  invden # gradient on numerator (i.e) partial derivative with respect to numerator on (8)
dinvden = num  # gradient on denominator on(8)
dden = (-1.0/(den**2))* dinvden
# backprop den = sigx + xpysqr
dsigx = 1 * dden                                                #(6)
dxpysqr = 1 * dden                                              #(6)
# backprop xpysqr = xpy**2
dxpy = (2 * xpy) * dxpysqr 
# backprop xpy = x + y
dx = (1) * dxpy                                                   #(4)
dy = (1) * dxpy                                                   #(4)
# backprop sigx = 1.0 / (1 + math.exp(-x))
dx += ((1 - sigx) * sigx) * dsigx # Notice += !! See notes below  #(3)
# backprop num = x + sigy
dx += (1) * dnum                                                  #(2)
dsigy = (1) * dnum                                                #(2)
# backprop sigy = 1.0 / (1 + math.exp(-y))
dy += ((1 - sigy) * sigy) * dsigy                                 #(1)

lister = [x, y, sigx, sigy, num, xpy, xpysqr, den, invden, f]

print(dx)
print(dy)
print(dsigx)
print(dsigy)
print(dnum)
print(dxpy)
print(dxpysqr)
print(dden)
print(dinvden)
print(f)