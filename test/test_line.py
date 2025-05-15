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

from bordado._line import line_coordinates, spacing_to_size


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
    ("size", "spacing"),
    [(10, None), (None, 0.1)],
)
def test_line_coordinates_passes(size, spacing):
    "Make sure no exceptions are raised for valid arguments"
    start, stop = 0, 1
    line_coordinates(start, stop, size=size, spacing=spacing)


@pytest.mark.parametrize(
    ("size", "spacing", "match"),
    [
        (None, None, "Either a size or a spacing"),
        (10, 0.1, "Both size and spacing"),
        (-1, None, "Invalid size"),
        (0, None, "Invalid size"),
    ],
)
def test_line_coordinates_fails(size, spacing, match):
    "Check failures for invalid arguments"
    start, stop = 0, 1
    with pytest.raises(ValueError, match=match):
        line_coordinates(start, stop, size=size, spacing=spacing)


@pytest.mark.parametrize(
    ("pixel_register", "adjust", "expected_coordinates"),
    [
        (False, "spacing", [0, 1]),
        (True, "spacing", [0.5]),
        (False, "region", [-1, 2]),
        (True, "region", [0.5]),
    ],
)
def test_line_coordinates_spacing_larger_than_twice_interval(
    pixel_register, adjust, expected_coordinates
):
    "Check if pixel_register works when the spacing is greater than the limits"
    coordinates = line_coordinates(
        0, 1, spacing=3, pixel_register=pixel_register, adjust=adjust
    )
    npt.assert_allclose(coordinates, expected_coordinates)
