import vtcode as vt
import Kernel_code as kc
import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from pandas.plotting import table


# pd.set_option('display.max_columns', None)
pd.options.display.max_columns = 10000000
pd.options.display.max_colwidth = 1000000
# pd.options.display.max_rows = 100000
pd.set_option('display.max_rows', None)
# pd.options.display.max_rows = 100000
n = int(input('Enter the length of the codeword: '))
binary_10_digit = vt.VTCode(n, 2, correct_substitutions=True)
length = binary_10_digit.k
Binary_number = []
Kernel_code = []
Concatenate_kernel_code = []
VT_encoded = []
pob = []
pob2 = []
for i in range(2 ** length):
    val = list(np.binary_repr(i, length))
    val = [int(x) for x in val]  # Converting the binary string to list into binary list
    Binary_number.append(val)  # Creating a list of binary from length k
    encoded_vt, [reverse_pob, dna_code, ker_code, con_ker_code] = binary_10_digit.encode(val)  # encoding using VT code
    Kernel_code.append(ker_code)
    Concatenate_kernel_code.append(con_ker_code)
    VT_encoded.append(encoded_vt)
    pob.append(dna_code)
    pob2.append(reverse_pob)
# print('Reverse_compliment_value of {} : {}'.format(n, vt.Kc.reverse_compliment_error(pob, pob2)))
mat_val = 2 * np.floor((n - 3) / 2)
# print('the matching value: ', mat_val)

DNA_code = pd.DataFrame([Binary_number, VT_encoded])
DNA_code1 = pd.DataFrame([Concatenate_kernel_code, pob])
DNA_code = DNA_code.transpose()
DNA_code1 = DNA_code1.transpose()
DNA_code.columns = ['Binary', 'VT_encoded']
DNA_code1.columns = ['Concatenate_kernel_code', 'DNA_code']

print(DNA_code)
print(DNA_code1)


df = DNA_code.copy()
