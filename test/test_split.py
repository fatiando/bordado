# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the coordinate splitting functions.

A large number of the unit tests are done as doctests in the function
docstrings.
"""

import pytest

from bordado._grid import grid_coordinates
from bordado._split import rolling_window, rolling_window_spherical


def test_rolling_window_size_too_large():
    "Make sure an exception is raised if the window size > region."
    region = (0, 1, 2, 4)
    coordinates = grid_coordinates(region, spacing=0.1)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window(coordinates, window_size=1.1, overlap=0.5)


def test_rolling_window_spherical_invalid_window_size():
    "Make sure an exception is raised if the window size is less than 0."
    region = (0, 1, 2, 4)
    coordinates = grid_coordinates(region, spacing=0.1)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window_spherical(coordinates, window_size=0, overlap=0.5)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window_spherical(coordinates, window_size=-0.1, overlap=0.5)
