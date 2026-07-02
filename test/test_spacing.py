# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the spacing related functions.
"""

import numpy.testing as npt
import pytest

from bordado._spacing import get_spacing, spacing_to_size


@pytest.mark.parametrize(
    ("spacing", "adjust", "expected_start", "expected_stop", "expected_size"),
    [
        (2.5, "spacing", -10, 0, 5),
        (2, "spacing", -10, 0, 6),
        (2.6, "spacing", -10, 0, 5),
        (2.4, "spacing", -10, 0, 5),
        (2.6, "region", -10.2, 0.2, 5),
        (2.4, "region", -9.8, -0.2, 5),
    ],
)
def test_spacing_to_size(spacing, adjust, expected_start, expected_stop, expected_size):
    "Check that correct size and stop are returned"
    start, stop = -10, 0
    size, new_start, new_stop = spacing_to_size(
        start, stop, spacing=spacing, adjust=adjust
    )
    npt.assert_allclose(size, expected_size)
    npt.assert_allclose(new_start, expected_start)
    npt.assert_allclose(new_stop, expected_stop)


def test_spacing_to_size_fails():
    "Check that invalid adjust causes an exception"
    with pytest.raises(ValueError, match="Invalid value for 'adjust'"):
        spacing_to_size(0, 1, spacing=0.1, adjust="invalid adjust value")


@pytest.mark.parametrize(
    "coordinates",
    [
        ([1, 2], [4, 5]),
        ([[1, 2], [4, 5]],),
        (
            [[1, 2], [4, 5]],
            [[1, 2], [4, 5]],
            [[1, 2], [4, 5]],
        ),
    ],
)
def test_get_spacing_fails_ndims(coordinates):
    "Check that the function errors when the coordinates have wrong dimensions"
    with pytest.raises(ValueError, match="Cannot extract spacing information"):
        get_spacing(coordinates)
