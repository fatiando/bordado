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

from ._validation import check_coordinates, check_dimensions, check_region


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
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape.

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
    coordinates = check_coordinates(coordinates)
    region = tuple(np.ravel([[np.min(c), np.max(c)] for c in coordinates]).tolist())
    return region


def inside(coordinates, region):
    """
    Determine which points fall inside a given region.

    Points at the boundaries are counted as being inside the region.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Should be in an
        order compatible with the order of boundaries in *region*. Arrays can
        be Python lists. Arrays can be of any shape but must all have the same
        shape.
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
    coordinates = check_coordinates(coordinates)
    ndims = len(region) // 2
    if len(coordinates) != ndims:
        message = (
            f"Invalid coordinates. Expected {ndims} coordinates for region '{region}' "
            f"but got {len(coordinates)} instead."
        )
        raise ValueError(message)
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


def rescale_coordinates(coordinates, region):
    """
    Rescale the coordinate values to fit the given region.

    Linearly transforms the input coordinates so that their minimum and maximum
    values match the lower and upper bounds of the provided *region*. The
    scaling is applied independently to each dimension.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Should be in an
        order compatible with the order of boundaries in *region*. Arrays can
        be Python lists. Arrays can be of any shape but must all have the same
        shape.
    region : tuple = (W, E, S, N, ...)
        The new boundaries for the region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.

    Returns
    -------
    rescaled_coordinates : tuple
        A tuple of arrays containing the rescaled coordinates. The returned
        arrays will have the same shape as the input coordinate arrays.

    Examples
    --------
    Let's demonstrate first using a single coordinate array:

    >>> import bordado as bd
    >>> coordinates = ([0, 5, 10],)

    These values can be stretched to a new range by providing a region
    like so:

    >>> rescaled_coordinates = rescale_coordinates(coordinates, [0, 100])
    >>> print(rescaled_coordinates)
    (array([  0.,  50., 100.]),)

    We can also translate coordinates. Note that if the original and
    new regions share the same dimensions, the rescaling simply acts as a pure
    translation of the points:

    >>> region = [10, 20]
    >>> rescaled_coordinates = rescale_coordinates(coordinates, region)
    >>> print(rescaled_coordinates[0])
    [10. 15. 20.]

    This also works for 2D coordinate arrays.
    Let's generate a 2D grid in an initial region (e.g., 3x3 points)

    >>> old_region = (0, 10, 0, 20)
    >>> east, north = bd.grid_coordinates(region=old_region, shape=(3, 3))

    Rescale the generated coordinates to a new target region

    >>> new_region = (0, 100, 0, 50)
    >>> new_east, new_north = rescale_coordinates((east, north), new_region)

    Generate the expected grid directly in the new region for comparison

    >>> expected_east, expected_north = bd.grid_coordinates(region=new_region, shape=(3, 3))

    Verify if the rescaled coordinates perfectly match the expected ones

    >>> print(new_east)
    [[  0.  50. 100.]
     [  0.  50. 100.]
     [  0.  50. 100.]]
    >>> print(expected_east)
    [[  0.  50. 100.]
     [  0.  50. 100.]
     [  0.  50. 100.]]

    >>> print(new_north)
    [[ 0.  0.  0.]
     [25. 25. 25.]
     [50. 50. 50.]]
    >>> print(expected_north)
    [[ 0.  0.  0.]
     [25. 25. 25.]
     [50. 50. 50.]]

    Note that the both east and north matches perfectely with the expected
    """
    check_region(region)
    coordinates = check_coordinates(coordinates)
    check_dimensions(coordinates, region)
    ndims = len(region) // 2
    old_region = get_region(coordinates)
    rescaled_coordinates = []
    for i, (coord_array, bounds_old, bounds_new) in enumerate(zip(
        coordinates, np.reshape(old_region, (ndims, 2)), np.reshape(region, (ndims, 2))
    )):
        min_old, max_old = bounds_old
        min_new, max_new = bounds_new
        diff_old = max_old - min_old
        diff_new = max_new - min_new
        if diff_old == 0 and diff_new != 0:
            message = (
                "Cannot rescale coordinates:"
                f"the original data has a range of {(bounds_old)}"
                f"of 0 in this dimensions: {ndims} (all values are identical), "
                f"but the target region requires a range of {(bounds_new)}."
                "Cannot rescale coordinate {i}. "
                f"The original data has a range of 0 (bounds = {bounds_old}) "
                f"but the target region requires a range of {diff_new} "
                f"(bounds = {bounds_new}), which is impossible to achieve."
            raise ValueError(message)
        scale = 0 if diff_old == 0 == diff_new else diff_new / diff_old
        new_coord = min_new + ((coord_array - min_old) * scale)
        rescaled_coordinates.append(new_coord)
    return tuple(rescaled_coordinates)
