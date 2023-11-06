import Kernel_code as kc
import numpy as np
import pandas as pd

# n = int(input('Enter the length of the codeword: '))
# length_info = n-1

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


for n in range(5, 20):
    Binary_number = []
    Kernel_code = []
    Concatenate_kernel_code = []
    pob = []
    pob2 = []
    length_info = n - 1
    for i in range(2**length_info):
        val = list(np.binary_repr(i, length_info))
        val = [
            int(x) for x in val
        ]  # Converting the binary string to list into binary list
        Binary_number.append(val)  # Creating a list of binary from length k
        Kc_b = kc.Kernel_codes()
        sep_values = Kc_b.kernel_code_encoder(val)
        pob2.append(sep_values[0])
        pob.append(sep_values[1])
        Kernel_code.append(sep_values[2])
        Concatenate_kernel_code.append(sep_values[3])

    DNA_code = pd.DataFrame([Binary_number, Kernel_code, Concatenate_kernel_code, pob])
    DNA_code = DNA_code.transpose()
    DNA_code.columns = [
        "Binary_number",
        "Kernel_code",
        "Concatenated kernel code",
        "DNA_codeword",
    ]
    # print(DNA_code)

    print(
        "Reverse_compliment_value of {} : {}".format(
            n, kc.reverse_compliment_error(pob, pob2)
        )
    )
    mat_val = 2 * np.floor((n - 3) / 2)
    print("the matching value: ", mat_val)
