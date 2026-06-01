# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the coordinate transformation functions.
"""

import numpy.testing as npt
import pytest

from bordado._region import get_region
from bordado._transform import rescale_coordinates


@pytest.mark.parametrize(
    ("coordinates", "region"),
    [
        (([10, 10], [0, 0]), [-10, 1, 1, 1]),
        (([10, 10], [0, 1]), [-10, 1, 1, 1]),
        (([15, 15], [1, 1]), [-15, -10, 1, 1]),
    ],
)
def test_rescale_coordinates_fails(coordinates, region):
    "Check if an exception is raised stretching coordinates with 0 spread"
    match = "Cannot rescale coordinate"
    with pytest.raises(ValueError, match=match):
        rescale_coordinates(coordinates, region)


@pytest.mark.parametrize(
    ("coordinates", "region"),
    [
        (([10, 10], [0, 0]), [-10, -10, 1, 1]),
        (([0, 0], [0, 0]), [-10, -10, 1, 1]),
        (([0, 0], [100, 100]), [-10, -10, 0, 0]),
    ],
)
def test_rescale_coordinates_translation(coordinates, region):
    "Check that translation only works when there 0 spread"
    rescaled = rescale_coordinates(coordinates, region)
    rescaled_region = get_region(rescaled)
    npt.assert_allclose(region, rescaled_region)
