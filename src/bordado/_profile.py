# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions to generate points along a segment between two points.
"""

import numpy as np

from ._line import line_coordinates


def profile_coordinates(
    beginning, end, *, size=None, spacing=None, non_dimensional_coords=None
):
    """
    Generate evenly spaced coordinates along a straight line between points.

    The generated coordinates specify points along a straight line in Cartesian
    space. The points are evenly spaced and can be specified by *size* (number
    of points) or their *spacing*. The points can be n-dimensional.

    Use this function to generates coordinates for sampling along a profile.

    Parameters
    ----------
    beginning : tuple = (easting, northing, ...)
        The coordinates of the starting point of the profile. Coordinates must
        be single values and not array-like.
    end : tuple = (easting, northing, ...)
        The coordinates of the ending point of the profile. Coordinates must be
        single values and not array-like.
    size : int or None
        The number of points in the profile. If None, *spacing* must be
        provided.
    spacing : float or None
        The step size (interval) between points in the profile. If None, *size*
        must be provided.
    non_dimensional_coords : None, scalar, or tuple of scalars
        If not None, then value(s) of extra non-dimensional coordinates
        (coordinates that aren't part of the profile dimensions, like height
        for a lat/lon profile). Will generate extra coordinate arrays from
        these values with the same shape of the final profile coordinates and
        the constant value given here. Use this to generate arrays of constant
        heights or times, for example, which might be needed to accompany
        a profile.

    Returns
    -------
    coordinates : tuple of arrays
        Arrays with coordinates of each point in the grid. Each array contains
        values for a dimension in the order of the given beginning and end
        points, and any extra values given in *non_dimensional_coords*. All
        arrays will be 1-dimensional and have the same shape.
    distances : array
        The coordinates of points along the straight line and the distances
        from the first point.

    Examples
    --------
    Generate a profile between two points with 11 points in it:

    >>> (east, north), dist = profile_coordinates((1, 10), (1, 20), size=11)
    >>> print('easting:', ', '.join(f'{i:.1f}' for i in east))
    easting: 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    >>> print('northing:', ', '.join(f'{i:.1f}' for i in north))
    northing: 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
    >>> print('distance:', ', '.join(f'{i:.1f}' for i in dist))
    distance: 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0

    We can equally specify the point spacing instead of the number of points:

    >>> (east, north), dist = profile_coordinates((1, 10), (1, 20), spacing=1)
    >>> print('easting:', ', '.join(f'{i:.1f}' for i in east))
    easting: 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    >>> print('northing:', ', '.join(f'{i:.1f}' for i in north))
    northing: 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
    >>> print('distance:', ', '.join(f'{i:.1f}' for i in dist))
    distance: 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0

    The points can also be more than 2-dimensional. The number of returned
    coordinates is the same as the number of input coordinates:

    >>> (east, north, up), dist = profile_coordinates(
    ...     (1, 10, 5), (1, 20, 5), spacing=1,
    ... )
    >>> print('easting:', ', '.join(f'{i:.1f}' for i in east))
    easting: 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    >>> print('northing:', ', '.join(f'{i:.1f}' for i in north))
    northing: 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0
    >>> print('upward:', ', '.join(f'{i:.1f}' for i in up))
    upward: 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
    >>> print('distance:', ', '.join(f'{i:.1f}' for i in dist))
    distance: 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0

    It can sometimes be useful to generate an additional array of the same size
    as the coordinates but filled with a single value, for example if doing
    a profile on easting and northing but we also need a constant height value
    returned:

    >>> (east, north, height), dist = profile_coordinates(
    ...     (1, 10), (1, 20), size=11, non_dimensional_coords=35)
    >>> print(height)
    [35. 35. 35. 35. 35. 35. 35. 35. 35. 35. 35.]

    You can specify multiple of these non-dimensional coordinates:

    >>> (east, north, height, time), dist = profile_coordinates(
    ...     (1, 10), (1, 20), size=11, non_dimensional_coords=(35, 0.1))
    >>> print(height)
    [35. 35. 35. 35. 35. 35. 35. 35. 35. 35. 35.]
    >>> print(time)
    [0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1 0.1]
    """
    if len(beginning) != len(end):
        message = (
            "Beginning and end points of the profile must have the same number of "
            f"coordinates. Given {len(beginning)} and {len(end)}, respectively."
        )
        raise ValueError(message)
    difference = np.asarray(end) - np.asarray(beginning)
    point_separation = np.sqrt(np.sum(difference**2))
    directional_vetor = difference / point_separation
    distances = line_coordinates(
        0, point_separation, size=size, spacing=spacing, adjust="spacing"
    )
    coordinates = [
        x + distances * direction for x, direction in zip(beginning, directional_vetor)
    ]
    if non_dimensional_coords is not None:
        for value in np.atleast_1d(non_dimensional_coords):
            coordinates.append(np.full_like(coordinates[0], value))
    return tuple(coordinates), distances
