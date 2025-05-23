# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the coordinate validation and manipulation functions.
"""

import pytest

from bordado._validation import check_coordinates, check_region, check_shape


@pytest.mark.parametrize(
    ("coordinates"),
    [
        ([1, 2], [[1, 2]]),
        ([1, 2], [[1], [2]]),
        ([[1], [2]], [1, 2]),
        ([[1, 2]], [1, 2]),
    ],
)
def test_check_coordinates_fails(coordinates):
    "Make sure the exception is raised for bad coordinates."
    with pytest.raises(ValueError, match="Invalid coordinates"):
        check_coordinates(coordinates)


@pytest.mark.parametrize(
    ("coordinates"),
    [
        ([[1, 2]], [[1, 2]]),
        ([[1], [2]], [[1], [2]]),
        ([[1], [2]], [[3], [4]]),
        ([[1, 2]], [[3, 4]]),
    ],
)
def test_check_coordinates_passes(coordinates):
    "Make sure no exception is raised for good coordinates."
    check_coordinates(coordinates)


@pytest.mark.parametrize(
    ("region", "message"),
    [
        ([], "Invalid region .* Must have an even"),
        ([1, 2, 3, 4, 5], "Invalid region .* Must have an even"),
        ([1, 2, 3], "Invalid region .* Must have an even"),
        ([1, 2, 3, 1], r"Invalid region .*: 1 \(3 > 1\)"),
        ([2, 1, 3, 4], r"Invalid region .*: 0 \(2 > 1\)"),
        ([2, 1, 3, 4, 7, 6], r"Invalid region .*: 0 \(2 > 1\); 2 \(7 > 6\)"),
    ],
)
def test_check_region_raises(region, message):
    "Make sure an exception is raised for bad regions."
    with pytest.raises(ValueError, match=message):
        check_region(region)


@pytest.mark.parametrize(
    "region",
    [
        [1, 2, 3, 4],
        [-2, -1, -5, -4],
        [-2, -1, -5, -4, 0, 1],
        [-2, -1, -5, -4, 0, 1, 10, 20],
    ],
)
def test_check_region_passes(region):
    "Check that valid regions don't cause exceptions."
    check_region(region)


@pytest.mark.parametrize(
    ("shape", "region"),
    [
        ([1, 2], []),
        ([], [1, 2, 3, 4]),
        ([1], [1, 2, 3, 4]),
        ([1, 2, 3], [1, 2, 3, 4]),
        ([], [1, 2, 3, 4, 5, 6]),
        ([1], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3, 4], [1, 2, 3, 4, 5, 6]),
    ],
)
def test_check_shape_raises(shape, region):
    "Make sure an exception is raised for bad regions."
    with pytest.raises(ValueError, match="Incompatible shape"):
        check_shape(shape, region)


@pytest.mark.parametrize(
    ("shape", "region"),
    [
        ([1], [1, 2]),
        ([1, 2], [1, 2, 3, 4]),
        ([1, 2, 3], [-2, -1, -5, -4, 0, 1]),
        ([1, 2, 3, 4], [-2, -1, -5, -4, 0, 1, 10, 20]),
    ],
)
def test_check_shape_passes(shape, region):
    "Check that valid regions and shapes don't cause exceptions."
    check_shape(shape, region)
