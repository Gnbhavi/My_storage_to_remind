import vtcode_copy as vt
import Kernel_code as kc
import numpy as np
import pandas as pd
import itertools

Kernel = kc.Kernel_codes()

# for n in range(12, 13):
# for n in range(7, 22):  
n = 12
binary_10_digit = vt.VTCode(n, 2, correct_substitutions=True)
length = binary_10_digit.k
length_before_kr = length-2
binary_rep = []
kerenel_val = []
redundancy_val = []
vt_total_encode =[]

  # m = 2 * n + 1

dict_map2 = {  # conversion map
            (0, 0): 'G',
            (0, 1): 'T',
            (1, 0): 'A',
            (1, 1): 'C'
        }
dict_map = {  # reverse construction map
            (0, 0): 'C',
            (0, 1): 'A',
            (1, 0): 'T',
            (1, 1): 'G'
        }


  
vt_encoded_val = []
redundancy_val = []
reversed_code = []
syndrome_val = []
DNA_code = []

for i in range(2**length_before_kr):
  val = list(np.binary_repr(i, length_before_kr))
  val = [int(x) for x in val]  # Converting the binary string to list into binary list
  parity = val.count(1) % 2
  value_kernel = [1] + val + [0] if parity else [1] + val + [1]

  redundancy = [0] * length

  

  """
        For the redundancy bit information bit is separated into 3 categories
  """
  redundancy[:int(np.floor((length - 1) / 2))] = value_kernel[:int(np.floor((length - 1) / 2))]
  hell = [(what + 1) % 2 for what in value_kernel[int(np.ceil((length - 1) / 2)):]]
  redundancy[int(np.ceil((length - 1) / 2)):] = hell
  if (length - 1) // 2:
    redundancy[int((length - 1) / 2)] = value_kernel[int((length - 1) / 2)] if parity else (1 + value_kernel[
                int((length - 1) / 2)]) % 2
  
  encoded_vt = binary_10_digit.encode(value_kernel)
  redundancy_enc = binary_10_digit.encode(redundancy)


  binary_rep.append(val)
  kerenel_val.append(value_kernel)
  vt_encoded_val.append(encoded_vt)

  redundancy_val.append(redundancy_enc)
  vt_total_encode.append( np.append(encoded_vt , redundancy_enc))

  iter_val = tuple(zip(encoded_vt, redundancy_enc))

  value = [dict_map2[element] for element in iter_val]  # reverse value is being stored for later use


  DNA_codeword = [dict_map[vals]for vals in iter_val]

  reversed_code.append(value[::-1])

  DNA_code.append(DNA_codeword)

  syndrome_val.append(binary_10_digit._is_codeword_new(np.array(redundancy_enc)))


  # if i == 19:
  #   print(val)
  #   print(value_kernel)
  #   print(redundancy) 
  #   print(encoded_vt)
  #   print(redundancy_enc)
  #   print(DNA_codeword)
    
Gc_content = [(elements.count('G') + elements.count('C'))/n for elements in DNA_code]
hello = pd.DataFrame([binary_rep, kerenel_val])
hello1 = pd.DataFrame([vt_encoded_val, redundancy_val, DNA_code])
# hello = pd.DataFrame([vt_encoded_val, redundancy_val, DNA_code, Gc_content, syndrome_val])
hello = hello.transpose()
hello1 = hello1.transpose()
# hello.columns= [' DNA']
hello.columns= ['Binary', 'Kernel encode']
hello1.columns = ['vt_encode', '', 'DNA code']
print(hello)
print(hello1)

pob_num = np.array(DNA_code)
hamming_matrix = [np.array(0)] * len(pob_num)
for i in range(len(pob_num)):
  y = pob_num != reversed_code[
            i]  # using numpy module checking the rows of whole matrix with one vector
  y = y.astype(int)  # Converting True false value as 0 and 1
  y = np.sum(y, axis=1)  # adding all the columns of each row to a single element
  hamming_matrix[i] = y


# print(binary_10_digit.decode(np.array([1,1,1,0,1,0,0,1,1,0,1])))
exit()


i = 19

val = list(np.binary_repr(i, length_before_kr))
val = [int(x) for x in val]  # Converting the binary string to list into binary list
parity = val.count(1) % 2
value_kernel = [1] + val + [0] if parity else [1] + val + [1]
encoded_vt = binary_10_digit.encode(value_kernel[:-1])

redundancy = [0] * length_before_kr


redundancy[:int(np.floor((length_before_kr - 1) / 2))] = val[:int(np.floor((length_before_kr - 1) / 2))]


hell = [(what + 1) % 2 for what in val[int(np.ceil((length_before_kr - 1) / 2)):]]
redundancy[int(np.ceil((length_before_kr - 1) / 2)):] = hell
if (length_before_kr - 1) // 2:
    redundancy[int((length_before_kr - 1) / 2)] = val[int((length_before_kr - 1) / 2)] if parity else (1 + val[
                int((length_before_kr - 1) / 2)]) % 2
    
redundancy = [value_kernel[-1]] + redundancy

encoded_vt = binary_10_digit.encode(value_kernel[:-1])
redundancy_enc = binary_10_digit.encode(redundancy)

print(val)

print("Kernel_encoded: ", value_kernel)
print("CK encoded: ", redundancy)
print("VT ENCODED")
print(encoded_vt)
print(redundancy_enc)
exit()








