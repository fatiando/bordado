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


def pad_region(region, pad):
    """
    Extend the borders of a region by the given amount.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.
    pad : float or tuple = (pad_WE, pad_SN, ...)
        The amount of padding to add to the region. If it's a single number,
        add this to all boundaries of region equally. If it's a tuple of
        numbers, then will add different padding to each dimension of the
        region respectively. If a tuple, the number of elements should be half
        of the number of elements in *region*.

    Returns
    -------
    padded_region : tuple = (W, E, S, N, ...)
        The padded region.

    Examples
    --------
    >>> pad_region((0, 1, -5, -3), 1)
    (-1, 2, -6, -2)
    >>> pad_region((0, 1, -5, -3, 6, 7), 1)
    (-1, 2, -6, -2, 5, 8)
    >>> pad_region((0, 1, -5, -3), (2, 3))
    (-2, 3, -8, 0)
    >>> pad_region((0, 1, -5, -3, 6, 7), (2, 3, 1))
    (-2, 3, -8, 0, 5, 8)

    """
    check_region(region)
    ndims = len(region) // 2
    if np.isscalar(pad):
        pad = tuple(pad for _ in range(ndims))
    if len(pad) != ndims:
        message = (
            f"Invalid padding '{pad}'. "
            f"Should have {ndims} elements for region '{region}'."
        )
        raise ValueError(message)
    region_pairs = np.reshape(region, (len(region) // 2, 2))
    padded = [[lower - p, upper + p] for p, (lower, upper) in zip(pad, region_pairs)]
    return tuple(np.ravel(padded).tolist())


def get_region(coordinates):
    """
    Get the bounding region of the given coordinates.

    Parameters
    ----------
    coordinates : tuple of arrays
        Arrays with the coordinates of each data point. Should be in the
        following order: (easting, northing, vertical, ...).

    Returns
    -------
    region : tuple = (W, E, S, N, ...)
        The boundaries that contain the coordinates. The order of lower and
        upper boundaries returned follows the order of *coordinates*.

    Examples
    --------
    >>> get_region(([0, 0.5, 1], [-10, -8, -6]))
    (0.0, 1.0, -10.0, -6.0)
    >>> get_region(([0, 0.5, 1], [-10, -8, -6], [4, 10, 16]))
    (0.0, 1.0, -10.0, -6.0, 4.0, 16.0)

    """
    region = tuple(np.ravel([[np.min(c), np.max(c)] for c in coordinates]).tolist())
    return region


def inside(coordinates, region):
    """
    Determine which points fall inside a given region.

    Points at the boundaries are counted as being inside the region.

    Parameters
    ----------
    coordinates : tuple of arrays
        Arrays with the coordinates of each data point. Should be in an order
        compatible with the order of boundaries in *region*.
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.

    Returns
    -------
    are_inside : array of booleans
        An array of booleans with the same shape as the input coordinate
        arrays. Will be ``True`` if the respective coordinates fall inside the
        area, ``False`` otherwise.

    Examples
    --------
    >>> east = [1, 2, 3, 4, 5, 6]
    >>> north = [10, 11, 12, 13, 14, 15]
    >>> region = (2.5, 5.5, 12, 15)
    >>> print(inside((east, north), region))
    [False False  True  True  True False]
    >>> # This also works for 2D-arrays
    >>> east = [[1, 2, 3],
    ...         [1, 2, 3],
    ...         [1, 2, 3]]
    >>> north = [[5, 5, 5],
    ...          [7, 7, 7],
    ...          [9, 9, 9]]
    >>> region = (0.5, 2.5, 7, 9)
    >>> print(inside((east, north), region))
    [[False False False]
     [ True  True False]
     [ True  True False]]
    >>> # and 3D-arrays or higher dimensions
    >>> east = [[[1, 2, 3],
    ...          [1, 2, 3],
    ...          [1, 2, 3]],
    ...         [[1, 2, 3],
    ...          [1, 2, 3],
    ...          [1, 2, 3]]]
    >>> north = [[[5, 5, 5],
    ...           [7, 7, 7],
    ...           [9, 9, 9]],
    ...          [[5, 5, 5],
    ...           [7, 7, 7],
    ...           [9, 9, 9]]]
    >>> up = [[[4, 4, 4],
    ...        [4, 4, 4],
    ...        [4, 4, 4]],
    ...       [[6, 6, 6],
    ...        [6, 6, 6],
    ...        [6, 6, 6]]]
    >>> region = (0.5, 2.5, 7, 9, 4.5, 7)
    >>> print(inside((east, north, up), region))
    [[[False False False]
      [False False False]
      [False False False]]
    <BLANKLINE>
     [[False False False]
      [ True  True False]
      [ True  True False]]]

    """
    check_region(region)
    ndims = len(region) // 2
    if len(coordinates) != ndims:
        message = (
            f"Invalid coordinates. Expected {ndims} coordinates for region '{region}' "
            f"but got {len(coordinates)} instead."
        )
        raise ValueError(message)
    coordinates = [np.asarray(c) for c in coordinates]
    region_pairs = np.reshape(region, (ndims, 2))
    shape = coordinates[0].shape
    # Allocate temporary arrays to minimize memory allocation overhead
    tmp = tuple(np.empty(shape, dtype=bool) for i in range(2))
    are_inside = np.full(shape, True)
    for coordinate, (lower, upper) in zip(coordinates, region_pairs):
        # Using the logical functions is a lot faster than & > < for some reason.
        # Plus, this way avoids repeated allocation of intermediate arrays by using
        # the "out" argument.
        in_dimension = np.logical_and(
            np.greater_equal(coordinate, lower, out=tmp[0]),
            np.less_equal(coordinate, upper, out=tmp[1]),
            out=tmp[0],
        )
        are_inside = np.logical_and(are_inside, in_dimension, out=are_inside)
    return are_inside
