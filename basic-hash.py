# basic-hash.py
import math

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
a0 = 3
b0 = 11
c0 = 36
d0 = 53
e0 = 7
f0 = 16

# message to hash
msg = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec iaculis tempor arcu, sit amet posuere turpis interdum non. 
		Pellentesque pellentesque neque eget felis dictum lacinia. Donec eget erat ante. 
		Mauris odio ex, ullamcorper sed convallis in, euismod sed turpis. Aliquam tristique luctus sem vitae consequat. 
		Nulla id leo fringilla, vulputate elit vitae, ultricies nisi. Maecenas porttitor nunc purus, in mattis lectus condimentum eget. 
		Donec sit amet condimentum ipsum, ac pretium lorem.'''
b_msg = list(x.encode('hex') for x in msg)

# last two bytes of message length value, used to pad
b_length = ''.join(list(bytes(len(b_msg)))[-2:])
print b_length, 'len check'

# pad byte array until % 8 == 0
while len(b_msg) % 8 != 0:
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

# final modulo addition
def mod_add(comb, const, chunk, f3):
	result = (comb + const) % pow(2, 32)
	result = (result + chunk) % pow(2, 32)
	result = (result + f3) % pow(2, 32)
	return result

# main cycle
def cycle(msg_64, const, b2, c2, d2, e2, f2, shift):
	global a0, b0, c0, d0, e0, f0

	b0 = mod_add(int(combination(b2, c2, d2, e2, f2)), const, int(''.join(msg_64), 16), f2) << shift
	c0 = b2
	d0 = c2
	e0 = d2
	f0 = e2
	a0 = f2

for i in range(len(msg_chunks)):
	cycle(msg_chunks[i], constants[i], b0, c0, d0, e0, f0, shifts[i])

print a0, b0, c0, d0, e0, f0
print "%x" % (a0 + b0 + c0 + d0 + e0 + f0)
