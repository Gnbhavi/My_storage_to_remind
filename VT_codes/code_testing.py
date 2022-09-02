import numpy as np
from Kernel_code import Kernel_codes

l = ['01101000', '01100101', '01101100', '01101100', '01101111', '00100000', '01100010', '01110101', '01100100', '01100100', 
            '01111001', '00100000', '01101000', '01101111', '01110111', '00100000', '01100001',
        '01110010', '01100101', '00100000', '01111001', '01101111', '01110101']

length = len(l)
enc = [0] * length 
kc = Kernel_codes()
for i in range(length):
    val = [int(x) for x in l[i]]
    _, enc[i], _, _= kc.kernel_code_encoder(val)
    print("i  = {}, enc is = {}".format(i, enc[i]))