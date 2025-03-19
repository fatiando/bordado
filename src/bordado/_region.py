# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for dealing with regions and bounding boxes.
"""
import numpy as np


def check_region(region):
    """
    Check that the given region dimensions are valid.

    There should be an even number of elements and lower boundaries should not
    be larger than upper boundaries.

    Parameters
    ----------
    region : list = [W, E, S, N, ...]
        The boundaries of a given region in Cartesian or geographic
        coordinates. Can contain more than 4 boundaries if the coordinates have
        more than 2 dimensions. Should have an even number of elements.

    Raises
    ------
    ValueError
        If the region doesn't have even number of entries and any lower
        boundary is larger than the upper boundary.

    """
    if len(region) % 2 != 0:
        message = (
        f"Invalid region '{region}'. Must have an even number of elements."
        )
        raise ValueError(message)
    offending = [lower > upper for lower, upper in np.reshape(region,
                                                              (len(region) //
                                                               2, 2))]
