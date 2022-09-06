import numpy as np
# import sys

class Rewritable_DNA_code:
    def __init__(self, a):
        self.a = a
        self.A = ['A', 'T', 'C']
    
    def A_bar(self, i, k = 0):
        A = ['A', 'C', 'T']
        if self.a[i] in A:
            A.remove(self.a[i])
        return A

    def Encode(self, l, x):
        n = len(self.a)
        S = self.S_val_calculator(n, l)
        if l >= n:
            t = 0
            y = x
            hell = len(self.A_bar(t)) * S[l - t - 2]
            while (y >= hell):
                y -= hell
                t += 1
                hell = len(self.A_bar(t)) * S[l - t - 2]
            c = y // S[l - t - 2]
            d = y % S[l - t - 2]
            what1 = self.a[ :t]
            what2 = [self.A_bar(t)[c]]
            what3 = self.Encode(l-t-1, d)
            return self.a[ :t] + [self.A_bar(t)[c]] + self.Encode(l-t-1, d)
        else :
            return self.theta(l, x) 


    def S_val_calculator(self, n, l):
        S = [0] * (l-1)
        for i in range(l-1):
            val = 0 
            if i < n - 1:
                S[i] = 3 ** (i+1)
            else:
                for k in range(n-1):
                    val = val +  len(self.A_bar(k)) * S[i-k-1]
                S[i] = val    
        return S

    def theta(self, l, x):
        enc_val = ['A'] * (l) 
        for j in range(l):
            rem_val = x % 3
            x = x // 3
            enc_val[l - j - 1] = self.A[rem_val]
        return enc_val





address_a = ['A', 'G', 'C', 'T', 'G']
RDc = Rewritable_DNA_code(address_a)
lets_see = RDc.Encode(8, 550)
# lets_see = RDc.S_val_calculator(5, 8)
# lets_see = RDc.theta(4, 16)
print((lets_see))
