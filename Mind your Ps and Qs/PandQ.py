from Crypto.Util.number import inverse, long_to_bytes

c = 964354128913912393938480857590969826308054462950561875638492039363373779803642185
n = 1584586296183412107468474423529992275940096154074798537916936609523894209759157543
e = 65537

# p and q from http://factordb.com/
p = 2434792384523484381583634042478415057961
q = 650809615742055581459820253356987396346063

phi = (p-1)*(q-1)


# a C code to get the private key d
# Private key (d stands for decrypt)
# choosing d such that it satisfies
# de(mod totient of n) = 1 --> d and e are the inverse of each other
# de=1 mod(ϕ(pq)) could be expressed as de=1+kϕ(pq) since in mod(ϕ(pq))
# adding kϕ(pq) is equivalent to adding a 0. i.e. kϕ(pq) in mod (ϕ(pq)) is 0.
# an easy example: (pq)*(k) mod(N) = 6*2 mod6 = 0
# d*e = 1 + k * totient
# int k = 2;  // can be a constant value - makes d larger
# double d = (1 + (k*phi))/e;
# d = (1 + (phi))/e


# python 3.8+
d = pow(e, -1, phi)

# for earlier versions

# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://www.youtube.com/watch?v=hB34-GSDT3k
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        # ax + by = gcd(a, b)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# https://www.youtube.com/watch?v=_bRVA5b4sb4
def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1: raise Exception('modular inverse does not exist')
    else: return x % m

# m = pow(c,d,n)

# print(long_to_bytes(m))

d = inverse(e, phi)

# decrypted
m = m2 = pow(c,d,n)

print(f"decrypted: {m}")
# byte string
m =long_to_bytes(m)
print(m)
# decoded string
m = m.decode('utf-8')
print(m)

# for letter in m: print(f"letter:{letter}, ascci:{ord(letter)} -->")
print(hex(m2))
# 0x7069636f4354467b736d6131315f4e5f6e305f67306f645f37333931383936327d
# 0x is no good so we just remove it
print(f"from hex: {bytearray.fromhex(hex(m2)[2:]).decode('utf-8')}")



print(f"\n{m2}\n")
m2 = str(m2)
n = len(m2)
arr = []
start = 0
for i, num in enumerate(m2):
    # if i == 0: continue
    # print(f"{start}-{i}:{m2[start:i + 1]}")
    if int(m2[start:i + 1]) > 127:
        arr.append(m2[start: i])
        start = i
print(arr)









# print(f"{n}, mod {n%4}")
# byte_array = list(0 for i in range(n // 4))
# for i in range(0, n, 4):
#     print(f"i:{i}, item:{m2[i:i + 4]}, int:{int(m2[i:i + 4])}")
#     # byte_array[i // 4] = m2[i:i + 4]
#     byte_array[i // 4] = int(m2[i:i + 4])
# print(f"\nbyte_array: {byte_array}")



# original_message = pow(int(c), int(d), int(n))
# print(f"int(n):{int(n)}\nint({int(c)})\nint({int(d)})\n\n")
# print(len(str(original_message)))
# print(original_message)

# # chr(X) converts an integer to a character