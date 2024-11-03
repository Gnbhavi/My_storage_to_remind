import random
import numpy as np
import pandas as pd
import vtcode_copy as vt
import Kernel_code as kc

def file_to_binary_string(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    # Convert each byte to an 8-bit binary representation and join them
    binary_string = ''.join(f'{byte:08b}' for byte in binary_data)
    return binary_string

def binary_string_to_file(binary_string, output_path):
    # Convert the binary string back to bytes
    byte_data = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    with open(output_path, 'wb') as file:
        file.write(byte_data)


def introduce_dna_errors(codewords, error_prob=0.02):
    # Define possible DNA bases
    dna_bases = ['A', 'T', 'G', 'C']
    
    modified_codewords = []
    
    for word in codewords:
        modified_word = []
        
        for base in word:
            if random.random() < error_prob:
                error_type = random.choice(['insert', 'delete', 'substitute'])
                
                if error_type == 'insert':
                    # Insert a random DNA base before the current base
                    modified_word.append(random.choice(dna_bases))
                    modified_word.append(base)
                elif error_type == 'delete':
                    # Skip the current base to delete it
                    continue
                elif error_type == 'substitute':
                    # Substitute with a random base different from the current one
                    new_base = random.choice([b for b in dna_bases if b != base])
                    modified_word.append(new_base)
            else:
                # No error, append the original base
                modified_word.append(base)
        
        # Join the modified characters to form the modified codeword
        modified_codewords.append("".join(modified_word))
    
    return modified_codewords


def count_differences(str1, str2):
    # Check if strings are of equal length
    if len(str1) != len(str2):
        raise ValueError("Strings must be of the same length to compare positions.")
    
    # Count differing positions
    differences = sum(1 for a, b in zip(str1, str2) if a != b)
    return differences



dict_map = {  # Converison map
            (0, 0): 'C',
            (0, 1): 'A',
            (1, 0): 'T',
            (1, 1): 'G'
        }


# Convert file to binary
file_path = "/Users/gnbhavithran/Downloads/acsnano.2c06748.pdf" # Replace with your file path
binary_data = file_to_binary_string(file_path)


# Processing and encoding the binary file
different_code_word_length = [15, 30, 45, 60, 75]  #going to encode in 14 length codeword
# error_rates = [0.009, 0.008, 0.007] # Putting different error rates
error_rates = [0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15] # Putting different error rates

# Create an empty DataFrame with n_values as index and error_rates as columns
df = pd.DataFrame(index=different_code_word_length, columns=error_rates)

for n in different_code_word_length:
  binary_14_digit = vt.VTCode(n, 2, correct_substitutions=True)
  information_length = binary_14_digit.k-2
  num_of_codewords_need_to_encode = int(np.ceil(len(binary_data)/information_length))

  DNA_code_pdf = []
  for batch in range(num_of_codewords_need_to_encode):
    val = [int(x) for x in binary_data[batch * information_length: ((batch+1) * information_length)]] # seprating into small blocks
    if len(val) != information_length:
      val = val + [0] * (information_length - len(val))
      print(val)
    parity = val.count(1) % 2
    value_kernel = [1] + val + [0] if parity else [1] + val + [1]
    redundancy = [0] * information_length
    """
          For the redundancy bit information bit is separated into 3 categories
    """
    redundancy[:int(np.floor((information_length - 1) / 2))] = value_kernel[:int(np.floor((information_length - 1) / 2))]
    redundancy_last_half = [(what + 1) % 2 for what in value_kernel[int(np.ceil((information_length - 1) / 2)):]]
    redundancy[int(np.ceil((information_length - 1) / 2)):] = redundancy_last_half
    if (information_length - 1) // 2:
      redundancy[int((information_length - 1) / 2)] = value_kernel[int((information_length - 1) / 2)] if parity else (1 + value_kernel[
                  int((information_length - 1) / 2)]) % 2

    encoded_vt = binary_14_digit.encode(value_kernel)
    redundancy_enc = binary_14_digit.encode(redundancy)

    iter_val = tuple(zip(tuple(encoded_vt), tuple(redundancy_enc)))

    DNA_codeword = [dict_map[vals]for vals in iter_val]
    DNA_codeword_str = ''.join(DNA_codeword)
    DNA_code_pdf.append(DNA_codeword_str)



  # Introducing errors and decoding

  decode_map ={
    'G' : 1,
    'C' : 0,
    'A' : 0,
    'T' : 1
  }



  for error_rate_values in error_rates:
    recived_message_with_error = introduce_dna_errors(DNA_code_pdf, error_prob=error_rate_values)
    binary_data_reconstruction = ''
    num_of_words_with_more_indel_error = 0
    num_bits_error = 0
    for i, code_words in enumerate(recived_message_with_error):
      binary_conversion_from_codeword = [decode_map[words] for words in code_words]
      Vt_decoding = binary_14_digit.decode(binary_conversion_from_codeword)
      if Vt_decoding is None:
        num_of_words_with_more_indel_error += 1
        continue
      Kernel_decoding = ''.join(map(str, Vt_decoding[1:-1]))
      binary_data_reconstruction = binary_data_reconstruction + Kernel_decoding
      if len(Kernel_decoding) != len(binary_data[i* information_length: (i+1)*information_length]):
        num_of_words_with_more_indel_error+=1
        continue
      num_bits_error += count_differences(binary_data[i* information_length: (i+1)*information_length], Kernel_decoding)
      df.at[n, error_rate_values] = (num_bits_error + (num_of_words_with_more_indel_error*information_length))/len(binary_data)
    print(df)
    print("For the codeword length {}, error occurance rate {} bit error rate is: {}".format(n, error_rate_values,(num_bits_error + (num_of_words_with_more_indel_error*information_length))/len(binary_data)))


df.to_csv("/Users/gnbhavithran/Python_github/My_storage_to_remind/VT_codes/error_rate_data_1.csv")



