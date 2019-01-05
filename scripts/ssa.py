#!/usr/bin/env python3

# Copyright (C) 2017-2019 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

from hashlib import sha256 as hf

from btclib.ec import pointMult
from btclib.ecurves import secp256k1 as ec

print("\n*** EC:")
print(ec)

q = 0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725
q = q % ec.n
print("\n*** Keys:")
print("prvkey:   ", hex(q))

Q = pointMult(ec, q, ec.G)
print("PubKey:", "02" if (Q[1] % 2 == 0) else "03", hex(Q[0]))

print("\n*** Message to be signed")
msg1 = "Paolo is afraid of ephemeral random numbers"
print(msg1)

print("*** Hash of the message")
h_bytes = hf(msg1.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
h1 = int.from_bytes(h_bytes, 'big') % ec.n
assert h1 != 0
print("    h1:", hex(h1))

print("\n*** Signature")
# ephemeral key k must be kept secret and never reused !!!!!
# good choice: k = hf(msg|q)
# different for each msg, private because of q
temp = msg1+hex(q)
k_bytes = hf(temp.encode()).digest()
k1 = int.from_bytes(k_bytes, 'big') % ec.n
assert k1 != 0

K1 = pointMult(ec, k1, ec.G)

s1 = (k1-h1*q) % ec.n
# if s1 == 0 (extremely unlikely for large ec.n) go back to a different ephemeral key
assert s1 != 0

print(" K1[0]:", hex(K1[0]))
print(" K1[1]:", hex(K1[1]))
print("    s1:", hex(s1))

print("*** Signature Verification")
minush1 = -h1 %ec.n
V = pointMult(ec, minush1, Q)
V = ec.add(K1, V)
print(V == pointMult(ec, s1, ec.G))

print("\n*** Another message")
msg2 = "and Paolo is right to be afraid"
print(msg2)

print("*** Hash of the message")
h_bytes = hf(msg2.encode()).digest()
# hash(msg) must be transformed into an integer modulo ec.n:
h2 = int.from_bytes(h_bytes, 'big') % ec.n
assert h2 != 0
print("    h2:", hex(h2))

print("\n*** Signature")
k2 = k1 #very bad! Never reuse the same ephemeral key!!!

K2 = pointMult(ec, k2, ec.G)

s2 = (k2-h2*q) %ec.n
# if s2 == 0 (extremely unlikely) go back to a different ephemeral key
assert s2 != 0

print(" K2[0]:", hex(K2[0]))
print(" K2[1]:", hex(K2[1]))
print("    s2:", hex(s2))

print("*** Signature Verification")
minush2 = -h2 %ec.n
V = pointMult(ec, minush2, Q)
V = ec.add(K2, V)
print(V == pointMult(ec, s2, ec.G))
