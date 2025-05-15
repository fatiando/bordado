# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the profile coordinate generating functions.
"""

import pytest

from bordado._profile import great_circle_coordinates, profile_coordinates


@pytest.mark.parametrize(("beginning", "end"), [((1, 2, 3), (1,)), ((1, 2), (1, 2, 3))])
def test_profile_coordinates_raises_invalid_points(beginning, end):
    "Make sure an exception is raised when input points are invalid"
    with pytest.raises(ValueError, match="Beginning and end points of the profile"):
        profile_coordinates(beginning, end, size=10)


@pytest.mark.parametrize(
    ("beginning", "end"),
    [
        ((1, 2, 3), (1, 2)),
        ((1, 2), (1, 2, 3)),
        ((1,), (1, 2)),
        ((1, 2), (1,)),
        ((1,), (1,)),
    ],
)
def test_great_circle_coordinates_raises_invalid_points(beginning, end):
    "Make sure an exception is raised when input points are invalid"
    with pytest.raises(ValueError, match="Beginning and end points of a great circle"):
        great_circle_coordinates(beginning, end, size=10)
