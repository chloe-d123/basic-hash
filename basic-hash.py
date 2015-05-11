# basic-hash.py
import math, sys

# first 64 primes
constants = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
			59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 
			137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 
			227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]

# binary shift values (random)
shifts = [4, 15, 16, 8, 1, 12, 10, 3, 6, 11, 5, 13, 2, 14, 7, 9,
		  7, 15, 6, 2, 14, 12, 4, 9, 11, 8, 1, 13, 16, 5, 10, 3,
		  11, 13, 16, 6, 8, 1, 10, 3, 15, 5, 14, 4, 2, 7, 9, 12,
		  13, 4, 7, 15, 8, 10, 3, 1, 12, 2, 16, 11, 9, 5, 6, 14]

# initialise variables (random)
a0 = 57
b0 = 82
c0 = 4
d0 = 30
e0 = 23
f0 = 2

# message to hash
f = open(sys.argv[1], 'rb')
msg = f.read()

b_msg = list(x.encode('hex') for x in msg)

# last two bytes of message length value, used to pad
b_length = ''.join(list(bytes(len(b_msg)))[-2:])
print b_length, 'length check byte'

# pad byte array until % 64 == 0
while len(b_msg) % 64 != 0:
	b_msg.append(b_length)
print len(b_msg), 'bytes'

# split message into chunks of 64 bits (8 bytes)
msg_chunks = []
temp = []
for i in range(len(b_msg)):
	temp.append(b_msg[i])
	if i % 8 == 7:						# 7 works. I don't know why.
		msg_chunks.append(temp)
		temp = []
print len(msg_chunks), 'chunks'

# combination function: ((b ^ c) | (d ^ e)) & f
def combination(b1, c1, d1, e1, f1):
	return ( ((bool(b1) ^ bool(c1)) | (bool(d1) ^ bool(e1))) & bool(f1) )

# final modulo addition. I don't know enough about modular arithmetic to say why 2^48 gives a 64-bit hash - but it does.
def mod_add(a3, comb, const, chunk, f3):
	result = (a3 + comb) % pow(2, 48)
	result = (result + chunk) % pow(2, 48)
	result = (result + const) % pow(2, 48)
    	result = (result + f3) % pow(2, 48)

	return result

# main cycle
def cycle(msg_64, const, a2, b2, c2, d2, e2, f2, shift):
	global a0, b0, c0, d0, e0, f0

	b0 = mod_add(a2, int(combination(b2, c2, d2, e2, f2)), const, int(''.join(msg_64), 16), f2) << shift
	c0 = b2
	d0 = c2
	e0 = d2
	f0 = e2
	a0 = f2

for i in range(len(msg_chunks)):
	cycle(msg_chunks[i], constants[i%64], a0, b0, c0, d0, e0, f0, shifts[i%64])

print "%x %x %x %x %x %x" % (a0, b0, c0, d0, e0, f0)
print "%x" % (a0 + b0 + c0 + d0 + e0 + f0)
