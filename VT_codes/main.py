import vtcode as vt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

n = int(input('Enter the length of the codeword: '))
binary_10_digit = vt.VTCode(n, 2, correct_substitutions=True)
length = binary_10_digit.k
Binary_number = []
Kernel_code = []
VT_encoded = []
pob = []
pob2 = []
pob_value = []
for i in range(2 ** length):
    val = list(np.binary_repr(i, length))
    val = [int(x) for x in val]  # Converting the binary string to list into binary list
    Binary_number.append(val)  # Creating a list of binary from length k
    encoded_vt, [kernel_subset, pob_val, dna_code] = binary_10_digit.encode(val)  # encoding using VT code
    VT_encoded.append(encoded_vt)
    Kernel_code.append(kernel_subset)
    pob.append(dna_code)
    pob_value.append(pob_val)

DNA_code = pd.DataFrame([Binary_number, VT_encoded, Kernel_code, pob_value, pob])
DNA_code = DNA_code.transpose()
DNA_code.columns = ['Binary_number', 'VT_encoded', 'Kernel_code', 'Concatenated Kernel Code', 'DNA_codeword']
print(DNA_code)
