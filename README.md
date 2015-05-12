# basic-hash.py

My attempt at a hash algorithm, in python. Loosely based on MD5.

Currently ~~nothing larger than 512 bytes can be hashed~~, and the 'avalanche' effect is very small.

The algorithm looks something like this:
```
The data to encode is represented in an array of bytes, and padded until the length is divisible by 8.
It is padded with the last two bytes of the value of its length.

The bytearray is then split into chunks of 8 bytes/64 bits. 
The first 64 primes are used as constants, and the variables a..f are random values.

The 'F' functions are: ((b ^ c) | (d ^ e)) & f
                       ((b ^ c ^ d) & ~e) | f
                       ((~b | c) ^ d) & (e ^ ~f)
                       (b | c | d) ^ (e & f)

b is set to the modulo 2^48 addition of a, F, the corresponding constant, a 64 bit chunk of the message, and f. This value is shifted left, by the corresponding number of bits in the table.

Then set c = b, d = c, e = d, f = e, and a = f.

After as many iterations as the data is long have occured, a..f are summed and returned as a hex number - this is the hash.
```

Usage: python basic-hash.py [file to hash]
