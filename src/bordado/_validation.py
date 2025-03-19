# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for validating inputs and outputs.
"""


def check_region(region):
    """
    Check that the given region dimensions are valid.

    West and South should not be greater than East and North, respectively.
    There should be 4 numbers.

    Parameters
    ----------
    region : list = [W, E, S, N]
        The boundaries of a given region in Cartesian or geographic
        coordinates.

    Raises
    ------
    ValueError
        If the region doesn't have exactly 4 entries, W > E, or S > N.

    """
    if len(region) != 4:
        message = f"Invalid region '{region}'. Only 4 values allowed."
        raise ValueError(message)
    w, e, s, n = region
    if w > e:
        message = (
            f"Invalid region '{region}' (W, E, S, N). Must have W <= E. "
            + "If working with geographic coordinates, don't forget to match geographic"
            + " region with coordinates using the 'longitude_continuity' function."
        )
        raise ValueError(message)
    if s > n:
        message = f"Invalid region '{region}' (W, E, S, N). Must have S <= N."
        raise ValueError(message)
