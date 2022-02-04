#!/usr/bin/python3 -u
import os.path

KEY_FILE = "key"
KEY_LEN = 50000
FLAG_FILE = "flag"


def startup(key_location):
	flag = open(FLAG_FILE).read()
	kf = open(KEY_FILE, "rb").read()

	start = key_location # equals 0
	stop = key_location + len(flag) # len(flag)=32 --> 0 + 32 = 32

	key = kf[start:stop]
	key_location = stop

	# the encryption here seems to be xoring the ord of a character from the flag
	# with the matching character from the key
	# remember that for each a, b the following process swaps a and b:
	# before: a = a, b = b --- *note*: a^b=b^a (essentialy the same)
	# a = a^b --> the difference between a and b
	# b = b^a --> the difference between b and (the difference between a and b) (which is a)
	# a = a^b --> the difference between (the difference between of a and b) and a (which is b)
	# after: a = b, b = a
	# meaning (a^b)^b = a, so similarly:
	# (a^b)^(a^c) = a -->
	# e_flag = key ^ flag
	# e_msg = key ^ msg
	# key = e_flag ^ e_msg
	# now we have to key, so all we have to do to get the flag is:
	# flag = key ^ e_flag (a^b^b = a where a=flag, b=key, a^b=e_flag)
	result = list( map( lambda p, k: "{:02x}".format(ord(p) ^ k), flag, key ) )
	print("This is the encrypted flag!\n{}\n".format("".join(result)))

	return key_location

def encrypt(key_location):
	ui = input("What data would you like to encrypt? ").rstrip()
	if len(ui) == 0 or len(ui) > KEY_LEN:
		return -1

	start = key_location # always equals the last run's stop key_location which is the stop
	stop = key_location + len(ui) # start + length of what we send

	kf = open(KEY_FILE, "rb").read()

	if stop >= KEY_LEN:
		stop = stop % KEY_LEN # if stop == KEY_LEN, stop = 0
		key = kf[start:] + kf[:stop]
	else:
		key = kf[start:stop]
	# make the key_location 0 to allow a repetition of the same key/pad as in the the first run (startup)
	key_location = stop 

	result = list(map(lambda p, k: "{:02x}".format(ord(p) ^ k), ui, key))

	print("Here ya go!\n{}\n".format("".join(result)))

	return key_location


print("******************Welcome to our OTP implementation!******************")
c = startup(0)
while c >= 0:
	c = encrypt(c)
