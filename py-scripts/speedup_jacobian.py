#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

import random
import time

from btclib.ec.curve import secp256k1 as ec
from btclib.ec.curve_group import mult_aff, mult_jac

random.seed(42)

# setup
qs = [random.getrandbits(ec.nlen) % ec.n for _ in range(50)]
start = time.time()
for q in qs:
    mult_aff(q, ec.G, ec)
elapsed1 = time.time() - start

start = time.time()
for q in qs:
    # starts from affine coordinates, ends with affine coordinates
    ec.aff_from_jac(mult_jac(q, ec.GJ, ec))
elapsed2 = time.time() - start

print(elapsed2 / elapsed1)
