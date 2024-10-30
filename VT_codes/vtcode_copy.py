import numpy as np
# import Kernel_code as Kc


class VTCode:
    def __init__(self, n: int, q: int, a=0, b=0,
                 correct_substitutions=False):
        """
        Here n is the codeword length and q is the alphabet size.
        a and b are parameters of the code that do not impact the rate in this
        implementation (so can be left at their default values).
        Set correct_substitutions to True for q = 2 if you want ability to correct
        single substitution errors as well.
        """
        assert q >= 2
        assert n >= 3
        self.n = n
        self.q = q
        assert q == 2
        self.correct_substitutions = correct_substitutions
        self.k = find_k(self.n, self.correct_substitutions)
        assert self.k > 0
        self.a = a
        self.b = b
        if not self.correct_substitutions:
            self.m = self.n + 1
        else:
            self.m = 2 * self.n + 1
        assert 0 <= self.a < self.m
        self._generate_systematic_positions_binary()
        # self.kc = Kc.Kernel_codes()

    def _generate_systematic_positions_binary(self):
        # generate positions of systematic and parity bits (1 indexed)
        t = np.ceil(np.log2(self.n + 1)).astype(np.int64)
        # put powers of two in the parity positions
        self.parity_positions = np.zeros(self.n - self.k, dtype=np.int64)
        for i in range(t):
            self.parity_positions[i] = np.power(2, i)
        if self.correct_substitutions:
            assert self.parity_positions.size == t + 1
            # one extra parity bit in this case
            # depending on if last position in codeword is already filled,
            # set it or the previous position as a parity_position
            if self.parity_positions[t - 1] == self.n:
                self.parity_positions[t - 1] = self.n - 1
                self.parity_positions[t] = self.n
            else:
                self.parity_positions[t] = self.n
        self.systematic_positions = np.setdiff1d(np.arange(1, self.n + 1), self.parity_positions)
        return

    def decode(self, y):
        """
        input  y: list or 1d np array with the noisy codeword
        return x: decoded message bits as a 1d numpy array with dtype int64 or
                  None if decoding fails
        """
        assert len(y) == 1
        # y = self.kc.kernel_code_decoder(z)
        print("Kernel code decoder: ", y)
        y = np.array(y, dtype=np.int64)
        n_y = y.size
        if (n_y < self.n - 1) or (n_y > self.n + 1):
            return None
        if (np.max(y) > self.q - 1) or (np.min(y) < 0):
            print("Value in y out of range 0...q-1")
            raise RuntimeError
        if n_y != self.n:
            y = _correct_binary_indel(self.n, self.m, self.a, y)

        else:
            if self.correct_substitutions and not self._is_codeword(y):
                y = _correct_binary_substitution(self.n, self.m, self.a, y)
        return self._decode_codeword(y)

    def _decode_codeword(self, y):
        """
        decode a codeword (if not a codeword, returns None)
        """
        if not self._is_codeword(y):
            return None
        return self._decode_codeword_binary(y)

    def _is_codeword(self, y):
        """
        return True if y is a codeword
        """
        if y is None or y.size != self.n:
            return False
        return _compute_syndrome_binary(self.m, self.a, y) == 0
        # return _compute_syndrome_binary(self.m, self.a, y)

        
    def _is_codeword_new(self, y):
        """
        return True if y is a codeword
        """
        if y is None or y.size != self.n:
            return False
        # return _compute_syndrome_binary(self.m, self.a, y) == 0
        return _compute_syndrome_binary(self.m, self.a, y)

    def encode(self, x):
        """
        input  x: list or 1d np array with the message bits (length k)
        return y: encoded codeword as a 1d numpy array with dtype int64 (length n)
        """
        x = np.array(x, dtype=np.int64)
        assert x.ndim == 1
        assert x.size == self.k
        if (np.max(x) > 1) or (np.min(x) < 0):
            print("Value in x out of range {0, 1}")
            raise RuntimeError
        vt_encode = self._encode_binary(x)
        return vt_encode
        # return self.kc.kernel_code_encoder(vt_encode)

    def _decode_codeword_binary(self, y):
        """
        decoding helper for binary case (assume it's a valid codeword)
        """
        # just return values at the systematic positions
        return y[self.systematic_positions - 1]

    def _encode_binary(self, x):
        """
        encoding helper for binary case
        """
        y = np.zeros(self.n, dtype=np.int64)
        # first set systematic positions
        y[self.systematic_positions - 1] = x
        # now set the rest positions based on syndrome
        syndrome = _compute_syndrome_binary(self.m, self.a, y)
        if syndrome != 0:
            for pos in reversed(self.parity_positions):
                if syndrome >= pos:
                    y[pos - 1] = 1
                    syndrome -= pos
                    if syndrome == 0:
                        break
        assert self._is_codeword(y)
        return y


def find_k(n: int, correct_substitutions=False):
    """
    Returns k for a code with given n and q.
    Here k is the message length in bits, n is the codeword length and q is the
    alphabet size.
    Set correct_substitutions to True for q = 2 if you want ability to correct
    single substitution errors as well.
    """
    if not correct_substitutions:
        h = n - np.ceil(np.log2(n + 1)).astype(np.int64)
        return h
    else:
        h = n - np.ceil(np.log2(2 * n + 1)).astype(np.int64)
        return h


def _correct_binary_substitution(n: int, m: int, a: int, y):
    """
    correct single substitution error in the binary case.
    Input: n (codeword length), m (modulus), a (syndrome),
           y (noisy codeword, np array)
    Output: corrected codeword
    """
    assert m == 2 * n + 1
    s = _compute_syndrome_binary(m, a, y)
    y_decoded = np.array(y)
    if s == 0:
        # no error, nothing to do
        pass
    elif s < n + 1:
        # 1 flipped to 0 at s
        y_decoded[s - 1] = 1
    else:
        # 0 flipped to 1 at 2n+1-s
        y_decoded[2 * n + 1 - s - 1] = 0
    return y_decoded


def _correct_binary_indel(n: int, m: int, a: int, y):
    """
    correct single insertion deletion error in the binary case.
    Used also in the q-ary alphabet case as a subroutine.
    Input: n (codeword length), m (modulus), a (syndrome),
           y (noisy codeword, np array)
    Output: corrected codeword
    """
    s = _compute_syndrome_binary(m, a, y)
    print("syndrome: ", s)
    w = np.sum(y)
    y_decoded = np.zeros(n, dtype=np.int64)
    if y.size == n - 1:
        # deletion
        if s == 0:
            # last entry 0 was deleted
            y_decoded[:-1] = y
        elif s <= w:
            # 0 deleted and s = number of 1s to right
            num_ones_seen = 0
            for i in reversed(range(n - 1)):
                if y[i] == 1:
                    num_ones_seen += 1
                    if num_ones_seen == s:
                        y_decoded[:i] = y[:i]
                        y_decoded[i + 1:] = y[i:]
                        break
        else:
            # 1 deleted and s-w-1 = number of 0s to left
            num_zeros_seen = 0
            if s - w - 1 == 0:
                y_decoded[0] = 1
                y_decoded[1:] = y
            else:
                success = False
                for i in range(n - 1):
                    if y[i] == 0:
                        num_zeros_seen += 1
                        if num_zeros_seen == s - w - 1:
                            y_decoded[:i + 1] = y[:i + 1]
                            y_decoded[i + 1] = 1
                            y_decoded[i + 2:] = y[i + 1:]
                            success = True
                            break
                if not success:
                    y_decoded = None
    else:
        # insertion
        if s == m - n - 1 or s == 0:
            # last entry inserted
            y_decoded = y[:-1]
        elif s == m - w:
            # remove first entry
            y_decoded = y[1:]
        elif s > m - w:
            # 0 was inserted, m-s 1's to the right of this zero
            num_ones_seen = 0
            success = False
            for i in reversed(range(2, n + 1)):
                if y[i] == 1:
                    num_ones_seen += 1
                    if num_ones_seen == m - s:
                        if y[i - 1] == 0:
                            y_decoded[:i - 1] = y[:i - 1]
                            y_decoded[i - 1:] = y[i:]
                            success = True
                        else:
                            pass
                        break
            if not success:
                y_decoded = None
        else:
            # 1 was inserted, m-w-s 0's to the left of this 1
            num_zeros_seen = 0
            success = False
            for i in range(n - 1):
                if y[i] == 0:
                    num_zeros_seen += 1
                    if num_zeros_seen == m - w - s:
                        if y[i + 1] == 1:
                            y_decoded[:i + 1] = y[:i + 1]
                            y_decoded[i + 1:] = y[i + 2:]
                            success = True
                        else:
                            pass
                        break
            if not success:
                y_decoded = None
    return y_decoded


def _compute_syndrome_binary(m: int, a: int, y):
    """
    compute the syndrome in the binary case (a - sum(i*y_i) mod m)
    """
    n_y = y.size
    
    return np.mod(a - np.sum((1 + np.arange(n_y)) * y), m)
  

"""
Now we are going to use kernel codes encoding and decoding
"""
