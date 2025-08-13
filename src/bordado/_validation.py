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


def check_coordinates_geographic(coordinates):
    """
    Check if geographic coordinates are within allowed bounds.

    Longitude boundaries should be in range [0, 360] or [-180, 180] and
    latitude boundaries should be in range [-90, 90].

    Parameters
    ----------
    coordinates : tuple = (longitude, latitude)
        Tuple of arrays with the longitude and latitude coordinates of each
        point. Arrays can be Python lists or any numpy-compatible array type.
        Arrays can be of any shape but must all have the same shape.

    Raises
    ------
    ValueError
        If the coordinates are outside their valid ranges or if there aren't
        exactly two coordinates.

    """
    if len(coordinates) != 2:
        message = (
            "Invalid coordinates. Must have exactly 2 elements"
            f" (longitude, latitude), but {len(coordinates)} were given."
        )
        raise ValueError(message)
    longitude, latitude = (np.atleast_1d(c) for c in coordinates)
    west, east = longitude.min(), longitude.max()
    south, north = latitude.min(), latitude.max()
    if west < -180 or east > 360 or (west < 0 and east > 180):
        message = (
            f"Invalid longitude range [{west}, {east}]. "
            "Longitude range must be [0, 360] or [-180, 180]."
        )
        raise ValueError(message)
    if south < -90 or north > 90:
        message = (
            f"Invalid latitude range [{south}, {north}]. "
            "Latitude range must be [-90, 90]."
        )
        raise ValueError(message)


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


def check_region_geographic(region):
    """
    Check that the given geographic region is valid.

    A region is a bounding box for 2-dimensional coordinates (W, E, S, N).
    There should be 4 elements and lower latitude boundaries should not be
    larger than upper boundaries. Longitude boundaries should be in range [0,
    360] or [-180, 180] and latitude boundaries should be in range [-90, 90].

    Parameters
    ----------
    region : tuple = (W, E, S, N)
        The boundaries of a given region in geographic coordinates. Should have
        a lower and an upper boundary for each dimension of the coordinate
        system.

    Raises
    ------
    ValueError
        If the region doesn't have 4 entries, any lower boundary is larger than
        the upper boundary, or boundaries are outside their valid ranges.

    """
    if not region or len(region) != 4:
        message = (
            f"Invalid region '{region}'. Must have exactly 4 elements"
            " (W, E, S, N), a lower and an upper boundary for each dimension."
        )
        raise ValueError(message)
    west, east, south, north = region
    if south > north:
        message = f"Invalid region '{region}'. South boundary must be less than north."
        raise ValueError(message)
    if west < -180 or east > 360 or (west < 0 and east > 180):
        message = (
            f"Invalid region '{region}'. Longitude range must be [0, 360] "
            "or [-180, 180]."
        )
        raise ValueError(message)
    if south < -90 or north > 90:
        message = f"Invalid region '{region}'. Latitude range must be [-90, 90]."
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


def check_overlap(overlap):
    """
    Check that the overlap argument is valid.

    It should be a decimal percentage in range [0, 1[. 100% overlap is not
    possible since that would generate infinite windows.

    Parameters
    ----------
    overlap : float
        The amount of overlap between adjacent windows. Should be within the
        range 1 > overlap ≥ 0.

    Raises
    ------
    ValueError
        In case the overlap is outside the allowed range.
    """
    if overlap < 0 or overlap >= 1:
        message = f"Invalid overlap '{overlap}'. Must be 1 > overlap >= 0."
        raise ValueError(message)


def longitude_continuity(region, *, coordinates=None):
    """
    Modify region boundaries and coordinates to ensure longitude continuity.

    Longitudinal boundaries of the region are moved to the ``[0, 360)`` or
    ``[-180, 180)`` degrees interval depending which one is better suited for
    that specific region to ensure that there are no discontinuities in the
    range. If given, coordinates are changed to match the new region.

    Longitude can be expressed as 0-360 or -180-180 and when specifying
    a small area, the longitude can have discontinuities in its range. For
    example, [350, 10] is a valid longitude range but wraps around at 0 instead
    of decreasing from 350 to 10. This can be problematic for some coordinate
    generation and manipulation routines.

    Parameters
    ----------
    region : tuple = (W, E, S, N)
        The boundaries of a given region in geographic coordinates. Should have
        a lower and an upper boundary for each dimension of the coordinate
        system.
    coordinates : tuple = (longitude, latitude) or None
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape. If None, we will assume that no
        coordinates are given.

    Returns
    -------
    modified_region : tuple = (W, E, S, N)
        The modified boundary of the region.
    modified_coordinates : tuple = (longitude, latitude)
        Only returned if coordinates are given. Modified set of geographic
        coordinates with continuous longitude.

    Examples
    --------
    Modify region with west > east to avoid the 360 discontinuity:

    >>> w, e, s, n = 350, 10, -10, 10
    >>> print(longitude_continuity([w, e, s, n]))
    (-10, 10, -10, 10)

    >>> w, e, s, n = 310, 180, -10, 10
    >>> print(longitude_continuity([w, e, s, n]))
    (-50, 180, -10, 10)

    For a global range of longitudes, always prefer the 0-360 range:

    >>> w, e, s, n = 0, 360, -10, 10
    >>> print(longitude_continuity([w, e, s, n]))
    (0, 360, -10, 10)

    >>> w, e, s, n = -180, 180, -10, 10
    >>> print(longitude_continuity([w, e, s, n]))
    (0, 360, -10, 10)

    Modify region and coordinates so that they match:

    >>> region = (350, 10, -60, -40)
    >>> coordinates = ((-10, -5, 0, 5, 10), (-60, -55, -50, -45, -40))
    >>> region, (longitude, latitude) = longitude_continuity(
    ...     region, coordinates=coordinates,
    ... )
    >>> print(region)
    (-10, 10, -60, -40)
    >>> print(longitude)
    [-10  -5   0   5  10]

    >>> region = (310, 180, -10, 10)
    >>> coordinates = ((310, 0, 180), (-10, 0, 10))
    >>> region, (longitude, latitude) = longitude_continuity(
    ...     region, coordinates=coordinates,
    ... )
    >>> print(region)
    (-50, 180, -10, 10)
    >>> print(longitude)
    [-50   0 180]

    The coordinates and region don't have to be within the same boundaries:

    >>> region = (-20, 20, -20, 20)
    >>> coordinates = ((0, 100, 200, 300), (-40, 0, 40, 80))
    >>> region, (longitude, latitude) = longitude_continuity(
    ...     region, coordinates=coordinates,
    ... )
    >>> print(region)
    (-20, 20, -20, 20)
    >>> print(longitude)
    [   0  100 -160  -60]
    """
    check_region_geographic(region)
    # Get longitudinal boundaries and check region
    w, e, s, n = region
    # Check if region is defined all around the globe
    all_globe = np.allclose(abs(e - w), 360)
    # Move coordinates to [0, 360)
    w = w % 360
    e = e % 360
    # Move west=0 and east=360 if region longitudes goes all around the globe
    if all_globe:
        w, e = 0, 360
    # Check if the [-180, 180) interval is better suited
    if w > e:
        interval_360 = False
        e = ((e + 180) % 360) - 180
        w = ((w + 180) % 360) - 180
        # If e = 180 then the above will create e=-180, which is wrong.
        # This only happens to the east limit and we need to fix it to have
        # a valid region.
        if e < w:
            e *= -1
    else:
        interval_360 = True
    modified_region = (w, e, s, n)
    if coordinates is not None:
        coordinates = check_coordinates(coordinates)
        check_coordinates_geographic(coordinates)
        # Run sanity checks for coordinates
        longitude = coordinates[0]
        longitude = longitude % 360
        if not interval_360:
            is_180 = np.isclose(longitude, 180)
            longitude = ((longitude + 180) % 360) - 180
            # Same as above when e < w leading to a -180 instead of 180.
            longitude[is_180] *= -1
        modified_coordinates = (longitude, *coordinates[1:])
        return modified_region, modified_coordinates
    return modified_region
