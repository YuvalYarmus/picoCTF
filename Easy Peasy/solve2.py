from pwn import *

import binascii

offset = 50000 - 32

r = remote('mercury.picoctf.net', 41934)

print(r.recvline())
print(r.recvline())
e_flag = r.recvline().strip()

print(f"\nencoded e_flag: {e_flag}, length: {len(e_flag)}")

r.recvuntil('?')
r.sendline('A'*offset)

r.recvuntil('?')

r.sendline('A'*32)

r.recvline()

encoded = r.recvline().strip()

print(f'encoded input: {encoded}')

encoded = binascii.unhexlify(encoded)

print(f'unhexed input: {encoded}')

print('--------------------------------------------------\nWorking on the decode\n--------------------------------------------------')

message = 'A'*32

key = []

for e in range(len(encoded)):
	key.append( ord(message[e])^encoded[e] )

print(f'[+] Found key: {key}')

print(f"message: {message}")
print(f"encoded: {encoded}")

e_flag = binascii.unhexlify(e_flag)
print(f"decoded e_flag: {e_flag}, length: {len(e_flag)}\n")

decoded_flag = []

for i in range(32):
	decoded_flag.append( chr(key[i]^e_flag[i]) )

flag = ''.join(decoded_flag)

print(f'flag: {flag}')