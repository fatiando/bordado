# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the grid coordinate generation functions.

Much of the functionality of grid_coordinates is tested in doctests in the
function docstring.
"""

import pytest

from bordado._grid import grid_coordinates


def test_grid_coordinates_fails_both_spacing_shape():
    "Check that an error is given when both a spacing and a shape are passed."
    with pytest.raises(ValueError, match="Both grid shape .* and spacing .*"):
        grid_coordinates((0, 1, 2, 3), spacing=0.1, shape=(5, 4))


def test_grid_coordinates_fails_no_spacing_shape():
    "Check that an error is given when neither spacing or shape are passed."
    with pytest.raises(ValueError, match="Either a grid shape or a spacing"):
        grid_coordinates((0, 1, 2, 3))


@pytest.mark.parametrize(
    ("region", "spacing"),
    [
        ((1, 2, 3, 4), (0.1,)),
        ((1, 2, 3, 4), (0.1, 0.2, 0.3)),
        ((1, 2, 3, 4, 5, 6), (0.1, 0.2)),
    ],
)
def test_grid_coordinates_fails_spacing_too_short(region, spacing):
    "Check that an error is given when spacing has too few elements."
    match = f"Invalid spacing .* Should have {len(region) // 2} values, .*"
    with pytest.raises(ValueError, match=match):
        grid_coordinates(region, spacing=spacing)
