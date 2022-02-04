hex_string = "0x70"

# Slice string to remove leading `0x`
hex_string = hex_string[2:]

# Convert to bytes object
bytes_object = bytes.fromhex(hex_string)

# Convert to ASCII representation
ascii_string = bytes_object.decode("ASCII")

print(ascii_string)

# the answer is p



/// another way:

hex_num = "0x70"
num = int(hex_num, 16) // num=112
string = chr(num) // string is 'p'

