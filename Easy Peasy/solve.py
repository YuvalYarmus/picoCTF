# import pwntools
from pwn import *
from binascii import unhexlify

# nc mercury.picoctf.net 41934

# # here I tried to see make the same encrypt with the same pad by 
# i = 97
# arr = []
# while i<102:
#     r = remote('mercury.picoctf.net', 41934)
#     r.recvuntil("This is the encrypted flag!\n")
#     enc_flag = r.recvline().decode()[:-1]
#     print(f"Encrypted flag: {enc_flag}, length: {len(enc_flag)}")
#     j = 0
#     arr_j = []
#     while j <= 2: 
#         r.recvuntil("What data would you like to encrypt?")
#         r.send(f"{chr(i)}\n")
#         r.recvline()
#         ans = r.recvline().decode()[:-1]
#         print(f"{chr(i)}: {ans}")
#         arr_j.append(f"{chr(i)}:{ans}")
#         j += 1

#     arr.append(arr_j)
#     r.close()
#     i += 1

# print(arr)

# decimal = []
# for  arr_j in arr:
#     decimal_j = []
#     for txt in arr_j:
#         split = txt.split(':')
#         hex = int(split[1], 16)
#         decimal_j.append(f"{split[0]}:{hex}")
#     decimal.append(decimal_j)

# print()
# print(decimal)

#  binascii.unhexlify(hexstr):
# Return the binary data represented by the hexadecimal string hexstr. 
# hexstr must contain an even number of hexadecimal digits (which can be upper or lower case),
# otherwise an Error exception is raised.

# the answer we get from recvline includes the newline so we use strip to remove it
KEY_LEN = 50000
FLAG_LEN = 32
OFFSET = KEY_LEN - FLAG_LEN

msg = 'A'*OFFSET
msg2 = 'A'*FLAG_LEN

r = remote('mercury.picoctf.net', 41934)
# r.recvuntil("This is the encrypted flag!\n")
print(r.recvline())
print(r.recvline())
# e_flag = r.recvline().decode()[:-1]
e_flag = r.recvline().strip()
print(f"\nencoded e_flag: {e_flag}, length: {len(e_flag)}")
print(e_flag)
e_flag = unhexlify(e_flag)
print(f"decoded e_flag: {e_flag}, length: {len(e_flag)}\n")

r.recvuntil('?')
r.sendline(msg)
r.recvline()
# e_msg = r.recvline().decode()[:-1]
e_msg = unhexlify(r.recvline().strip())

r.recvuntil('?')
r.sendline(msg2)
r.recvline()
# e_msg2 = r.recvline().decode()[:-1]
e_msg2 = r.recvline().strip()
print(f"\nencoded e_msg2: {e_msg2}")
e_msg2 = unhexlify(e_msg2)
print(f"decoded e_msg2: {e_msg2}\n")

print(f"e_flag:{e_flag}, e_msg2:{e_msg2}\n")
# we want the same key/one time pad that was used on the flag, the first one to decrypt the flag
# we first sent a message as long as the offset to reset the key so that it will be the same key
# as in the first one that encrypts the next message
# and then we sent a message as long as the flag (msg2) which was encrypted using the same key as the first one
# now we are getting the key using xor rules:
# get the key using the rule (a^b)^b = a --> (msg^key)^msg=key ---> (e_msg)^msg=key
# can also get it (I think) by the rule (a^b)^(a^c)=a --> (msg^key)^(flag^key)=key --->
# (e_msg)^(e_flag)=key

# key1 = ""
# key2 = ""
# didnt work well as string because the result of each action is a 2 digit number
key1 = []
key2 = []

for i, letter in enumerate(msg2):
    # print(f"letter:{letter}, e_msg2:{e_msg2[i]}")
    # print(f"e_msg2 is: {e_msg2} \ne_msg2[i]:{e_msg2[i]}")
    key1.append(ord(letter)^e_msg2[i])

for i, letter in enumerate(e_msg2):
    key2.append(letter^e_flag[i])


print(f"key1 == key2: {key1 == key2}")
if key1 != key2:
    print(f"key1:{key1}\n")
    print(f"key2:{key2}\n")

# now to decrypt the flag we need to xor it with the key:
flag = ""
for i, letter in enumerate(e_flag):
    flag += chr(letter^key1[i])
    if i > 31:
        print("Reached")
        break

print(f"flag = {flag}")