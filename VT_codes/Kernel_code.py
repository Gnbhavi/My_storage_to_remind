# from ast import Return
import numpy as np


class Kernel_codes:
    def __init__(self):
        self.dict_map2 = {  # conversion map
            (0, 0): 'G',
            (0, 1): 'T',
            (1, 0): 'A',
            (1, 1): 'C'
        }
        self.dict_map = {  # reverse construction map
            (0, 0): 'C',
            (0, 1): 'A',
            (1, 0): 'T',
            (1, 1): 'G'
        }
        self.decode_book = {  # as per the name decoding helper
            'G': 1,
            'T': 1,
            'C': 0,
            'A': 0
        }

    def kernel_code_encoder(self, word):
        word = list(word)
        enc_k = len(word)
        redundancy = [0] * enc_k  # Adding the redundancy for the bits
        parity = word.count(1) % 2  # the parity finder for encoding
        value_kernel = [1] + word + [0] if parity else [1] + word + [1]
        """
        For the redundancy bit information bit is separated into 3 categories
        """
        redundancy[:int(np.floor((enc_k - 1) / 2))] = word[:int(np.floor((enc_k - 1) / 2))]
        hell = [(what + 1) % 2 for what in word[int(np.ceil((enc_k - 1) / 2)):]]
        redundancy[int(np.ceil((enc_k - 1) / 2)):] = hell
        if (enc_k - 1) // 2:
            redundancy[int((enc_k - 1) / 2)] = word[int((enc_k - 1) / 2)] if parity else (1 + word[
                int((enc_k - 1) / 2)]) % 2
        the_value = value_kernel + redundancy  # The redundancy bit is attached to the encoding values
        iter_val = tuple(
            zip(the_value[:enc_k + 1], the_value[enc_k + 1:]))  # tupling the respective values to encode into DNA
        dna_codeword = [self.dict_map[element] for element in iter_val]  # the tuple is converted into DNA
        value = [self.dict_map2[element] for element in iter_val]  # reverse value is being stored for later use
        reverse_compliment_codeword = value[::-1]
        return reverse_compliment_codeword, dna_codeword, value_kernel, the_value
        # return dna_codeword

    def kernel_code_decoder(self, received_word):
        decode_kernel = [self.decode_book[value] if value in self.decode_book else ValueError
                         for value in received_word]
        return decode_kernel[1:]


def reverse_compliment_error(pob, pob2):
    pob_num = np.array(pob)
    hamming_matrix = [np.array(0)] * len(pob_num)
    for i in range(len(pob_num)):
        y = pob_num != pob2[
            i]  # using numpy module checking the rows of whole matrix with one vector
        y = y.astype(int)  # Converting True false value as 0 and 1
        y = np.sum(y, axis=1)  # adding all the columns of each row to a single element
        hamming_matrix[i] = y
    return np.min(hamming_matrix)


def correlation_finder(A, B):
    C = [0] * len(A)
    for i in range(len(A)):
        val = 0
        j = 0
        while (j < len(B) and i+j < len(A)):
            if A[i+j] == B[j]:
                val = 1
                break
            j += 1
        C[i] = val
    return C
