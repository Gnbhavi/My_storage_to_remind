A = ['1', '2', '3']
B = ['2', '3', '4']
C = ['0'] * 3
for i in range(len(A)):
    val = '0'
    j = 0
    while(j < len(B) and i+j < len(A)):
        if A[i+j] == B[j]:
            val = '1'
            break
        j += 1
    C[i] = val
print(C)