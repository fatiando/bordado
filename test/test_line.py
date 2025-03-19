# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the coordinate generation functions.
"""

import numpy.testing as npt
import pytest

from bordado._line import _spacing_to_size, line_coordinates


@pytest.mark.parametrize(
    ("spacing", "adjust", "expected_stop", "expected_size"),
    [
        (2.5, "spacing", 0, 5),
        (2, "spacing", 0, 6),
        (2.6, "spacing", 0, 5),
        (2.4, "spacing", 0, 5),
        (2.6, "region", 0.4, 5),
        (2.4, "region", -0.4, 5),
    ],
)
def test_spacing_to_size(spacing, adjust, expected_stop, expected_size):
    "Check that correct size and stop are returned"
    start, stop = -10, 0
    size, new_stop = _spacing_to_size(start, stop, spacing=spacing, adjust=adjust)
    npt.assert_allclose(size, expected_size)
    npt.assert_allclose(new_stop, expected_stop)


def test_spacing_to_size_fails():
    "Check that invalid adjust causes an exception"
    with pytest.raises(ValueError, match="Invalid value for 'adjust'"):
        _spacing_to_size(0, 1, spacing=0.1, adjust="invalid adjust value")


def test_line_coordinates_fails():
    "Check failures for invalid arguments"
    start, stop = 0, 1
    size = 10
    spacing = 0.1
    # Make sure it doesn't fail for these parameters
    line_coordinates(start, stop, size=size)
    line_coordinates(start, stop, spacing=spacing)
    with pytest.raises(ValueError, match="Either a size or a spacing"):
        line_coordinates(start, stop)
    with pytest.raises(ValueError, match="Both size and spacing"):
        line_coordinates(start, stop, size=size, spacing=spacing)


def test_line_coordinates_spacing_larger_than_twice_interval():
    "Check if pixel_register works when the spacing is greater than the limits"
    start, stop = 0, 1
    spacing = 3
    coordinates = line_coordinates(start, stop, spacing=spacing)
    npt.assert_allclose(coordinates, [0, 1])
    coordinates = line_coordinates(start, stop, spacing=spacing, pixel_register=True)
    npt.assert_allclose(coordinates, [0.5])
    coordinates = line_coordinates(start, stop, spacing=spacing, adjust="region")
    npt.assert_allclose(coordinates, [0, 3])
    coordinates = line_coordinates(
        start, stop, spacing=spacing, pixel_register=True, adjust="region"
    )
    npt.assert_allclose(coordinates, [1.5])
