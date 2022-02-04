flag = "hello!"
new_flag = ''.join([chr((ord(flag[i]) << 8) + ord(flag[i + 1])) for i in range(0, len(flag), 2)])
print(new_flag)
for i in range(0, len(flag), 2):
    print(f"og: {flag[i]}-{flag[i + 1]}={ord(flag[i])}-{ord(flag[i + 1])}")
    print(f"new: {ord(new_flag[i // 2])}")
    print(f"decode half: {chr(ord(new_flag[i // 2]) >> 8)}={(ord(new_flag[i // 2]) >> 8)}")


flag = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸強㕤㐸㤸扽"

new_flag = ""
for i in range(len(flag)):
    new_flag += chr((ord(flag[i]) >> 8))

print(f"\n{new_flag}\n")

# half the characters are missing

# now we need to get the second half
# we know that each character was added the ascci number of its following (now missing) character
# right of the bat that implicates we need to subtract an ord of something to undo it.

# lets an example:
# we have got the part from "hello!" which o! o=111 !=33
# 111 << 8 + 33 is 28449 which is needed the ascci of the new character
# if we do  28449 >> 8 we get 111 again.
# now if we once again perfrom 11 << 8 we get 28416
# if we subtract 28416 which is actually the shifted letter o,
# from the encoded character's ascci (28449) which is o!,
# we get the 33 which is the ! missing.
# >>> n = ((111 << 8) + 33)
# >>> n
# 28449
# >>> n2 = n
# >>> n2
# 28449
# >>> n2 >> 8
# 111
# >>> n2 - (n2 >> 8)
# 28338
# >>> n2 - (n2 >> 8)<<8
# 7254528
# >>> n2 - ((n2 >> 8)<<8)
# 33

encoded_string = "灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸強㕤㐸㤸扽"
decoded_string = ""
for i in range(len(encoded_string)):
    # the first half we already knew how to decode
    decoded_string += chr(ord(encoded_string[i])>>8)
    # creating the second half
    decoded_string += chr(ord(encoded_string[i]) - ((ord(encoded_string[i]) >> 8)<<8) )
    

print(decoded_string)