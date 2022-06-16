import vtcode as vt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

binary_10_digit = vt.VTCode(20, 2, correct_substitutions=True)
length = binary_10_digit.k
Binary_number = []
Kernel_code = []
VT_encoded = []
pob = []
pob2 = []
dict_map_2 = {
    (0, 0): 'G',
    (0, 1): 'T',
    (1, 0): 'A',
    (1, 1): 'C'
}
for i in range(2 ** length):
    val = list(np.binary_repr(i, length))
    val = [int(x) for x in val]  # Converting the binary string to list into binary list
    Binary_number.append(val)  # Creating a list of binary from length k
    encoded_vt, [kernel_subset, dna_code] = binary_10_digit.encode(val)  # encoding using VT code
    VT_encoded.append(encoded_vt)
    Kernel_code.append(kernel_subset)
    pob.append(dna_code)

DNA_code = pd.DataFrame([Binary_number, VT_encoded, Kernel_code, pob])
DNA_code = DNA_code.transpose()
DNA_code.columns = ['Binary_number', 'VT_encoded', 'Kernel_code', 'DNA_codeword']
# print(pob)
reverse_complement_number = binary_10_digit.kc.reverse_compliment_error(pob)
ran_val = np.random.randint(0, 2**length)
print('Random Value', ran_val)
print('information: {}, encoded: {}'.format(Binary_number[ran_val], pob[ran_val]))
print('Decoded: ', binary_10_digit.decode(pob[ran_val]))
print('reverse_complement_number:', reverse_complement_number)
