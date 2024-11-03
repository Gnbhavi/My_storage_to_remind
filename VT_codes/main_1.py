import vtcode as vt
import Kernel_code as kc
import numpy as np
import pandas as pd
import itertools

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

n = int(input('Enter the length of the codeword: '))
binary_10_digit = vt.VTCode(n, 2, correct_substitutions=True)
length = binary_10_digit.k
val = list(np.binary_repr(11, length))
val = [int(x) for x in val]
print("K value: ", length)
print("Binary representation of 11: ", val)
encoded_vt, [reverse_pob, dna_code, ker_code, con_ker_code] = binary_10_digit.encode(val)  # encoding using VT code
print(dna_code)

recived_dna_code = dna_code.copy()
recived_dna_code.pop(3)
print(recived_dna_code)
print(len(recived_dna_code))
dna_code_corrected = binary_10_digit.decode(recived_dna_code)
print("Corrected DNA code: ", dna_code_corrected)