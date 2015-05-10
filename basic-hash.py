# basic-hash.py
import math, sys

# first n primes
def get_primes(n):
    numbers = set(range(n, 1, -1))
    primes = []
    while numbers:
        p = numbers.pop()
        primes.append(p)
        numbers.difference_update(set(range(p*2, n+1, p)))
    return primes

constants = []

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
f = open(sys.argv[1], 'r')
msg = f.read()

b_msg = list(x.encode('hex') for x in msg)

# last two bytes of message length value, used to pad
b_length = ''.join(list(bytes(len(b_msg)))[-2:])
print b_length, 'len check'

# pad byte array until % 8 == 0
while len(b_msg) % 8 != 0:
	b_msg.append(b_length)
print len(b_msg), 'bytes'

# generate required primes
constants = get_primes(len(b_msg))

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
def mod_add(a3, comb, const, chunk, f3):
	result = (a3 + comb) % pow(2, 32)
	result = (result + chunk) % pow(2, 32)
	result = (result + const) % pow(2, 32)
    	result = (result + f3) % pow(2, 32)

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
	cycle(msg_chunks[i], constants[i], a0, b0, c0, d0, e0, f0, shifts[i%64])

print hex(a0), hex(b0), hex(c0), hex(d0), hex(e0), hex(f0)
print "%x" % (a0 + b0 + c0 + d0 + e0 + f0)
