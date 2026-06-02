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

import numpy as np
import pytest

from bordado._grid import grid_coordinates
from bordado._split import (
    block_split_spherical,
    rolling_window,
    rolling_window_spherical,
)


def test_rolling_window_size_too_large():
    "Make sure an exception is raised if the window size > region."
    region = (0, 1, 2, 4)
    coordinates = grid_coordinates(region, spacing=0.1)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window(coordinates, window_size=1.1, overlap=0.5)


def test_rolling_window_size_too_large_higher_dim():
    "Window size check should apply to all region dimensions, not just the first two."
    coordinates = (
        np.array([-2.0, 0.0, 2.0]),
        np.array([-2.0, 0.0, 2.0]),
        np.array([-0.5, 0.0, 0.5]),
    )
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window(coordinates, window_size=2, overlap=0.5)


def test_rolling_window_spherical_invalid_window_size():
    "Make sure an exception is raised if the window size is less than 0."
    region = (0, 1, 2, 4)
    coordinates = grid_coordinates(region, spacing=0.1)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window_spherical(coordinates, window_size=0, overlap=0.5)
    with pytest.raises(ValueError, match="Invalid window size"):
        rolling_window_spherical(coordinates, window_size=-0.1, overlap=0.5)


@pytest.mark.parametrize("block_size", [0, -10])
def test_block_split_spherical_invalid_block_size(block_size):
    "Check that an error is raised for invalid block_size"
    coordinates = grid_coordinates(region=(0, 360, -90, 90), spacing=10)
    with pytest.raises(ValueError, match="Invalid block size"):
        block_split_spherical(coordinates, block_size)
