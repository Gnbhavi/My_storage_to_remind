import numpy as np
from Kernel_code import Kernel_codes
import codecs

# l = ['01101000', '01100101', '01101100', '01101100', '01101111', '00100000', '01100010', '01110101', '01100100', '01100100', 
#             '01111001', '00100000', '01101000', '01101111', '01110111', '00100000', '01100001',
#         '01110010', '01100101', '00100000', '01111001', '01101111', '01110101']


# input_message = input("Enter the word to convert into Kernel Code: ")
datafile=open("/Users/gnbhavithran/Downloads/2022_IJBIC-106227.pdf",'rb')
pdfdatab=datafile.read()    #this is binary data
b64PDF = codecs.encode(pdfdatab, 'base64')
input_message=b64PDF.decode('utf-8')
l = [format(ord(x), 'b') for x in input_message]

length = len(l)
enc = [0] * length 
kc = Kernel_codes()
for i in range(length):
    val = [int(x) for x in l[i]]
    _, enc[i], _, _= kc.kernel_code_encoder(val)

# for hello in range(10):
#     print("i  = {}, enc is = {}".format(hello, enc[hello]))

print(len(enc))