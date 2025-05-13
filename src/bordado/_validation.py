# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for validating inputs and outputs.
"""

import numpy as np


def check_coordinates(coordinates):
    """
    Check that coordinate arrays all have the same shape.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape.

    Returns
    -------
    coordinates : tuple = (easting, northing, ...)
        Tuple of coordinate arrays, converted to numpy arrays if necessary.

    Raises
    ------
    ValueError
        If the coordinates don't have the same shape.
    """
    coordinates = tuple(np.asarray(c) for c in coordinates)
    shapes = [c.shape for c in coordinates]
    if not all(shape == shapes[0] for shape in shapes):
        message = (
            "Invalid coordinates. All coordinate arrays must have the same shape. "
            f"Given coordinate shapes: {shapes}"
        )
        raise ValueError(message)
    return coordinates


def check_region(region):
    """
    Check that the given region is valid.

    A region is a bounding box for n-dimensional coordinates. There should be
    an even number of elements and lower boundaries should not be larger than
    upper boundaries.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.

    Raises
    ------
    ValueError
        If the region doesn't have even number of entries and any lower
        boundary is larger than the upper boundary.

    """
    if not region or len(region) % 2 != 0:
        message = (
            f"Invalid region '{region}'. Must have an even number of elements, "
            "a lower and an upper boundary for each dimension."
        )
        raise ValueError(message)
    region_pairs = np.reshape(region, (len(region) // 2, 2))
    offending = [lower > upper for lower, upper in region_pairs]
    if any(offending):
        bad_bounds = []
        for dimension, is_bad in enumerate(offending):
            if is_bad:
                lower, upper = region_pairs[dimension]
                bad_bounds.append(f"{dimension} ({lower} > {upper})")
        message = (
            f"Invalid region '{region}'. Lower boundary larger than upper boundary "
            f"in dimension(s): {'; '.join(bad_bounds)}"
        )
        raise ValueError(message)


def check_adjust(adjust, valid=("spacing", "region")):
    """
    Check if the adjust argument is valid.

    Parameters
    ----------
    adjust : str
        The value of the adjust argument given to a function.
    valid : list or tuple
        The list of valid values for the argument.

    Raises
    ------
    ValueError
        In case the argument is not in the list of valid values.
    """
    if adjust not in valid:
        message = (
            f"Invalid value for 'adjust' argument '{adjust}'. Should be one of {valid}."
        )
        raise ValueError(message)


def check_shape(shape, region):
    """
    Check if the shape has a number of elements compatible with the region.

    The shape should have ``len(region) / 2`` elements. Assumes that the region
    is valid.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.
    shape : tuple = (..., size_SN, size_WE)
        The number of points in each direction of the given region, in reverse
        order. Must have one integer value per dimension of the region. The
        order of arguments is the opposite of the order of the region for
        compatibility with numpy's ``.shape`` attribute.

    Raises
    ------
    ValueError
        In case the number of elements in the shape is incorrect.
    """
    if not shape or not region or len(shape) != len(region) / 2:
        message = (
            f"Incompatible shape '{shape}' and region '{region}. "
            "There must be one element in 'shape' of every two elements in 'region'."
        )
        raise ValueError(message)
