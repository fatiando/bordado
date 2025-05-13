# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the input and output validation functions.
"""

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from bordado._region import get_region, inside, pad_region


@pytest.mark.parametrize(
    ("region", "pad"),
    [
        ([1, 2, 3, 4], (1,)),
        ([1, 2, 3, 4], (1, 2, 3)),
        ([-2, -1, -5, -4, 0, 1], (1,)),
        ([-2, -1, -5, -4, 0, 1], (1, 2)),
        ([-2, -1, -5, -4, 0, 1], (1, 2, 3, 4)),
        ([-2, -1, -5, -4, 0, 1, 10, 20], (1,)),
        ([-2, -1, -5, -4, 0, 1, 10, 20], (1, 2)),
        ([-2, -1, -5, -4, 0, 1, 10, 20], (1, 2, 3)),
        ([-2, -1, -5, -4, 0, 1, 10, 20], (1, 2, 3, 4, 5)),
    ],
)
def test_pad_region_fails(region, pad):
    "Check if an exception is raised for invalid padding."
    with pytest.raises(ValueError, match="Invalid padding"):
        pad_region(region, pad)


@pytest.mark.parametrize(
    ("region", "coordinates"),
    [
        ([1, 2, 3, 4], ([1, 2],)),
        ([1, 2, 3, 4], ([1, 2], [1, 2], [1, 2])),
        ([-2, -1, -5, -4, 0, 1], ([1, 2],)),
        ([-2, -1, -5, -4, 0, 1], ([1, 2], [1, 2])),
        ([-2, -1, -5, -4, 0, 1], ([1, 2], [1, 2], [1, 2], [1, 2])),
    ],
)
def test_inside_fails_len_coordinates(region, coordinates):
    "Check if an exception is raised when there are too few coordinates"
    match = f"Expected {len(region) // 2} .* got {len(coordinates)} .*"
    with pytest.raises(ValueError, match=match):
        inside(coordinates, region)


@pytest.mark.parametrize(
    "coordinates",
    [
        (np.array([1.0, 2.0, 3.0]), np.array([1.0, 2.0, 3.0])),
        (pd.Series([1.0, 2.0, 3.0]), pd.Series([1.0, 2.0, 3.0])),
        (xr.DataArray([1.0, 2.0, 3.0]), xr.DataArray([1.0, 2.0, 3.0])),
    ],
)
def test_get_region_array_dtypes(coordinates):
    "Make sure the region has floats and not arrays or numpy dtypes"
    region = get_region(coordinates)
    assert all(isinstance(i, float) for i in region)
