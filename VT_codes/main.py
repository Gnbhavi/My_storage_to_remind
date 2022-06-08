import vtcode as vt

binary_10_digit = vt.VTCode(10, 2, correct_substitutions=True)
print(binary_10_digit.k)
print(binary_10_digit.encode([0, 1, 0, 0, 1]))
print(binary_10_digit.decode([1, 1, 0, 1, 1, 0, 0, 0, 1, 0]))
