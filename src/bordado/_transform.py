# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for transforming coordinates.
"""

import numpy as np

from ._region import get_region
from ._validation import check_coordinates, check_dimensions, check_region


def rescale_coordinates(coordinates, region):
    """
    Rescale the coordinate values to fit the given region.

    Linearly transforms the input coordinates so that their minimum and maximum
    values match the lower and upper bounds of the provided *region*. The
    scaling is applied independently to each coordinate.

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
    Let's demonstrate first using a single coordinate array. The coordinates
    must be specified as a tuple of arrays.

    >>> import bordado as bd
    >>> coordinates = ([0, 5, 10],)

    These values can be stretched to a new range by providing a region like so:

    >>> rescaled_coordinates = rescale_coordinates(coordinates, [0, 100])
    >>> print(rescaled_coordinates)
    (array([  0.,  50., 100.]),)

    We can also translate coordinates. Note that if the original and new regions
    share the same length, the rescaling simply acts as a pure translation of
    the points:

    >>> region = [10, 20]
    >>> rescaled_coordinates = rescale_coordinates(coordinates, region)
    >>> print(rescaled_coordinates)
    (array([10., 15., 20.]),)

    This also works for 2D coordinate arrays (or any number of dimensions).
    Let's generate coordinates for a 2D grid:

    >>> coordinates = bd.grid_coordinates(region=(0, 10, 0, 20), shape=(3, 3))
    >>> print(coordinates[0])
    [[ 0.  5. 10.]
     [ 0.  5. 10.]
     [ 0.  5. 10.]]
    >>> print(coordinates[1])
    [[ 0.  0.  0.]
     [10. 10. 10.]
     [20. 20. 20.]]

    Rescale the generated coordinates to a new target region happens for each
    coordinate independently:

    >>> rescaled = rescale_coordinates(coordinates, (0, 100, 0, 50))
    >>> print(rescaled[0])
    [[  0.  50. 100.]
     [  0.  50. 100.]
     [  0.  50. 100.]]
    >>> print(rescaled[1])
    [[ 0.  0.  0.]
     [25. 25. 25.]
     [50. 50. 50.]]

    """
    check_region(region)
    coordinates = check_coordinates(coordinates)
    check_dimensions(coordinates, region)
    ndims = len(region) // 2
    # Reshape the region so we can iterate over min,max pairs
    region = np.reshape(region, (ndims, 2))
    region_old = np.reshape(get_region(coordinates), (ndims, 2))
    rescaled_coordinates = []
    for i in range(ndims):
        min_old, max_old = region_old[i]
        min_new, max_new = region[i]
        diff_old = max_old - min_old
        diff_new = max_new - min_new
        if diff_old == 0 and diff_new != 0:
            message = (
                f"Cannot rescale coordinate {i}. "
                f"The original data has a range of 0 (bounds = ({min_old}, {max_old})) "
                f"but the target region requires a range of {diff_new} "
                f"(bounds = ({min_new}, {max_new})), which is impossible to achieve."
            )
            raise ValueError(message)
        scale = 0 if diff_old == 0 == diff_new else diff_new / diff_old
        new_coord = min_new + ((coordinates[i] - min_old) * scale)
        rescaled_coordinates.append(new_coord)
    return tuple(rescaled_coordinates)


def rotate_coordinates(coordinates, angle):
    r"""
    Rotate coordinates in 2-dimensional space.

    Apply a `rotation matrix <https://en.wikipedia.org/wiki/Rotation_matrix>`__`
    to the vectors defined by the given coordinates in a 2D space. The rotation
    is **counterclockwise**.

    Parameters
    ----------
    coordinates : tuple = (easting, northing)
        Tuple of arrays with the coordinates of each point. Should have **2
        elements**. Arrays can be Python lists. Arrays can be of any shape but
        must all have the same shape.
    angle : float
        The angle of rotation in degrees.

    Returns
    -------
    rotated_coordinates : tuple
        A tuple of arrays containing the rotated coordinates. The returned
        arrays will have the same shape as the input coordinate arrays.

    Examples
    --------
    Let's say we have points that fall on a line along the first dimension:

    >>> coordinates = ([1, 2, 3], [0, 0, 0])

    Rotating these points by 90° should align them with the second dimension:

    >>> rotated = rotate_coordinates(coordinates, angle=90)
    >>> print("First coordinate:", ", ".join(f"{x:.2f}" for x in rotated[0]))
    First coordinate: 0.00, 0.00, 0.00
    >>> print("Second coordinate:", ", ".join(f"{x:.2f}" for x in rotated[1]))
    Second coordinate: 1.00, 2.00, 3.00

    And rotating them clockwise (-90°) should align them with the negative part
    of the second dimension:

    >>> rotated = rotate_coordinates(coordinates, angle=-90)
    >>> print("First coordinate:", ", ".join(f"{x:.2f}" for x in rotated[0]))
    First coordinate: 0.00, 0.00, 0.00
    >>> print("Second coordinate:", ", ".join(f"{x:.2f}" for x in rotated[1]))
    Second coordinate: -1.00, -2.00, -3.00

    The coordinates can have any shape but there can only be 2 of them:

    >>> coordinates = ([[1, 2], [3, 4]], [[0, 0], [0, 0]])
    >>> rotated = rotate_coordinates(coordinates, angle=90)
    >>> for line in rotated[0]:
    ...     print(", ".join(f"{x:.2f}" for x in line))
    0.00, 0.00
    0.00, 0.00
    >>> for line in rotated[1]:
    ...     print(", ".join(f"{x:.2f}" for x in line))
    1.00, 2.00
    3.00, 4.00

    """
    coordinates = check_coordinates(coordinates)
    ndims = len(coordinates)
    if ndims != 2:
        message = (
            f"Cannot rotate {ndims} coordinates. "
            "Only works in 2D and hence can only take 2 coordinate arrays."
        )
        raise ValueError(message)
    angle = np.radians(angle)
    cos = np.cos(angle)
    sin = np.sin(angle)
    rotated = (
        cos * coordinates[0] - sin * coordinates[1],
        sin * coordinates[0] + cos * coordinates[1],
    )
    return rotated
