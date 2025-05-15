# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test distance calculation functions for nearest neighbors.
"""

import pytest

from bordado._distance import neighbor_distance_statistics
from bordado._grid import grid_coordinates


@pytest.mark.parametrize("k", [0, -1])
def test_neighbor_distance_statistics_raises_invalid_k(k):
    "Check that an exception is raised for invalid inputs"
    coordinates = grid_coordinates((5, 10, -20, -17), spacing=1)
    with pytest.raises(ValueError, match="Invalid number of neighbors"):
        neighbor_distance_statistics(coordinates, statistic="mean", k=k)


@pytest.mark.parametrize("statistic", ["bla", "mena"])
def test_neighbor_distance_statistics_raises_invalid_statistic(statistic):
    "Check that an exception is raised for invalid inputs"
    coordinates = grid_coordinates((5, 10, -20, -17), spacing=1)
    with pytest.raises(ValueError, match="Invalid statistic"):
        neighbor_distance_statistics(coordinates, statistic, k=4)


@pytest.mark.parametrize("statistic", ["mean", "median", "std", "var", "ptp"])
def test_neighbor_distance_statistics_valid_statistic(statistic):
    "Check that an exception is not raised for valid inputs"
    coordinates = grid_coordinates((5, 10, -20, -17), spacing=1)
    neighbor_distance_statistics(coordinates, statistic, k=5)
