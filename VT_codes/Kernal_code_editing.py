# import vtcode as vt
import Kernel_code as Kc
import numpy as np
import pandas as pd
import itertools

# pd.set_option('display.max_columns', None)
pd.options.display.max_columns = 10000000
pd.options.display.max_colwidth = 1000000

pd.set_option('display.max_rows', None)

k = int(input('Enter the length of the codeword: '))
kc =Kc.Kernel_codes()
Binary_number = []
Kernel_code = []
Concatenate_kernel_code = []
# VT_encoded = []
pob = []
pob2 = []
for i in range(2 ** k):
    val = list(np.binary_repr(i, k))
    val = [int(x) for x in val]  # Converting the binary string to list into binary list
    Binary_number.append(val)  # Creating a list of binary from length k
    reverse_pob, dna_code, ker_code, con_ker_code = kc.kernel_code_encoder(val)  # encoding using VT code
    Kernel_code.append(ker_code)
    Concatenate_kernel_code.append(con_ker_code)
    # VT_encoded.append(encoded_vt)
    pob.append(dna_code)
    pob2.append(reverse_pob)
# print('Reverse_compliment_value of {} : {}'.format(n, vt.Kc.reverse_compliment_error(pob, pob2)))
# mat_val = 2 * np.floor((n - 3) / 2)
# print('the matching value: ', mat_val)

DNA_code = pd.DataFrame([Binary_number, Kernel_code])
DNA_code1 = pd.DataFrame([Concatenate_kernel_code, pob])
DNA_code = DNA_code.transpose()
DNA_code1 = DNA_code1.transpose()
DNA_code.columns = ['Binary_number', 'Kernel Code']
DNA_code1.columns = ['Concatenate_kernel_code', 'DNA_code']
# print(len(pob))

# Lets_see = []
# for i, j in itertools.combinations(pob, 2):
#     Lets_see.append(sum(kc.correlation_finder(i, j)))

# print(np.max(Lets_see))
print(DNA_code)
print(DNA_code1)
