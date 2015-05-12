# basic-hash.py

My attempt at a hash algorithm, in python. Loosely based on MD5.

Currently 'avalanche' effect is fine for changes in length, but very small when swapping single bytes.

The algorithm looks something like this:
```
The data to encode is represented in an array of bytes, and padded until the length is 
	divisible by 256.
It is padded with the last two bytes of the value of its length.

The bytearray is then split into chunks of 4 bytes/32 bits. 
The first 64 primes are used as constants, and the variables a..f are random values.

The 'F' functions are: ((b ^ c) | (d ^ e)) & f
                       ((b ^ c ^ d) & ~e) | f
                       ((~b | c) ^ d) & (e ^ ~f)
                       (b | c | d) ^ (e & f)

b is set to the modulo 2^64 addition of a, F, the corresponding constant, 
	a 64 bit chunk of the message, and f. This value is shifted left, by the 
	corresponding number of bits in the table.

Then set c = b, d = c, e = d, f = e, and a = f.

After as many iterations as the data is long have occured, a..f are summed 
	and returned as a 20 char/80 bit hex number - this is the hash.
```

Usage: python basic-hash.py [file to hash].

Currently, this is **slow**. Probably due to being written in python and my inability to optimise.