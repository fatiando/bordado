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

from bordado._coordinates import check_coordinates


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
