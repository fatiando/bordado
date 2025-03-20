# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the random coordinate generation functions.
"""

import numpy as np
import numpy.testing as npt

from bordado._random import get_rng


def test_get_rng_none():
    "Check that the random number generator is not seeded"
    result1 = get_rng(None).uniform(0, 1, 10)
    result2 = get_rng(None).uniform(0, 1, 10)
    assert not np.allclose(result1, result2)


def test_get_rng_int():
    "Check that the random number generator is seeded"
    result1 = get_rng(1).uniform(0, 1, 10)
    result2 = get_rng(1).uniform(0, 1, 10)
    npt.assert_allclose(result1, result2)


def test_get_rng_custom_rng():
    "Check that passing a Generator works"
    # Using the same RNG should not lead to identical sequences
    random = np.random.default_rng(10)
    result1 = get_rng(random).uniform(0, 1, 10)
    result2 = get_rng(random).uniform(0, 1, 10)
    assert not np.allclose(result1, result2)
    # But seeding the RNG equally twice should
    result1 = get_rng(np.random.default_rng(10)).uniform(0, 1, 10)
    result2 = get_rng(np.random.default_rng(10)).uniform(0, 1, 10)
    npt.assert_allclose(result1, result2)
