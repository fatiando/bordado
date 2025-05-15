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
        Arrays with coordinates of each point in the profile. Each array
        contains values for a dimension in the order of the given beginning and
        end points, and any extra values given in *non_dimensional_coords*. All
        arrays will be 1-dimensional and have the same shape.
    distances : array
        The straight-line distances between each point in the profile and the
        beginning point.

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


def great_circle_coordinates(
    beginning,
    end,
    *,
    size=None,
    spacing=None,
    radius=6_370_994,
    non_dimensional_coords=None,
):
    """
    Generate evenly spaced coordinates along a great circle between points.

    The beginning and end points must be (longitude, latitude) coordinates on
    a sphere. The generated coordinates will be evenly spaced (in physical
    distances, not degrees) and fall along a great circle path between the two
    points. The points can be specified by *size* (number of points) or their
    *spacing* (in physical units, like meters).

    Use this function to generates coordinates for sampling along a profile
    when data are in geographic coordinates.

    Parameters
    ----------
    beginning : tuple = (longitude, latitude)
        The coordinates of the starting point of the profile. Coordinates must
        be single values and not array-like. Units should be decimal degrees.
    end : tuple = (longitude, latitude)
        The coordinates of the ending point of the profile. Coordinates must be
        single values and not array-like. Units should be decimal degrees.
    size : int or None
        The number of points in the profile. If None, *spacing* must be
        provided.
    spacing : float or None
        The step size (interval) between points in the profile. If None, *size*
        must be provided. Units should be compatible with *radius*
        (usually meters).
    radius : float
        The radius of the sphere, usually the mean radius of the Earth or other
        body used to scale the distances along the great circle. Units should
        be compatible with *spacing* (usually meters). Defaults to the mean
        radius of the WGS84 Earth ellipsoid (6,370,994 meters).
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
    coordinates : tuple = (longitude, latitude, ...)
        Arrays with the coordinates of each point in the profile. The first two
        are longitude and latitude. Subsequent arrays are any extra values
        given in *non_dimensional_coords*. All arrays will be 1-dimensional and
        have the same shape.
    distances : array
        The great circle distances between each point in the profile and the
        beginning point.

    Examples
    --------
    Generate coordinates between points at the equator for a sphere with a unit
    radius:

    >>> import numpy as np
    >>> spacing = 2 * np.pi / 180
    >>> (longitude, latitude), distance = great_circle_coordinates(
    ...     (0, 0), (10, 0), spacing=spacing, radius=1,
    ... )
    >>> print('longitude:', ', '.join(f'{i:.1f}' for i in longitude))
    longitude: 0.0, 2.0, 4.0, 6.0, 8.0, 10.0
    >>> print('latitude:', ', '.join(f'{i:.1f}' for i in latitude))
    latitude: 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    >>> print('distance:', ', '.join(f'{i:.4f}' for i in distance))
    distance: 0.0000, 0.0349, 0.0698, 0.1047, 0.1396, 0.1745
    >>> print(np.allclose(distance[1:] - distance[0:-1], spacing))
    True

    It can sometimes be useful to generate an additional array of the same size
    as the coordinates but filled with a single value, for example if  we also
    need a constant height value returned:

    >>> (lon, lat, height), dist = great_circle_coordinates(
    ...     (1, 10), (1, 20), size=11, non_dimensional_coords=35)
    >>> print(height)
    [35. 35. 35. 35. 35. 35. 35. 35. 35. 35. 35.]
    """
    if len(beginning) != 2 or len(end) != 2:
        message = (
            "Beginning and end points of a great circle profile must have two "
            "coordinates (longitude and latitude). "
            f"Given {beginning} and {end}, respectively."
        )
        raise ValueError(message)
    lon1, lat1 = np.radians(beginning)
    lon2, lat2 = np.radians(end)
    coslon = np.cos(lon2 - lon1)
    sinlon = np.sin(lon2 - lon1)
    coslat1 = np.cos(lat1)
    sinlat1 = np.sin(lat1)
    coslat2 = np.cos(lat2)
    sinlat2 = np.sin(lat2)
    # These are needed to calculate the lon/lat coordinates of the profile.
    # See https://en.wikipedia.org/wiki/Great-circle_navigation#Finding_way-points
    azimuth1 = np.arctan2(
        coslat2 * sinlon, coslat1 * sinlat2 - sinlat1 * coslat2 * coslon
    )
    sinazimuth1 = np.sin(azimuth1)
    cosazimuth1 = np.cos(azimuth1)
    azimuth_equator = np.arctan2(
        sinazimuth1 * coslat1, np.sqrt(cosazimuth1**2 + sinazimuth1**2 * sinlat1**2)
    )
    sinazimuth_equator = np.sin(azimuth_equator)
    cosazimuth_equator = np.cos(azimuth_equator)
    great_circle_equator = np.arctan2(np.tan(lat1), cosazimuth1)
    lon_equator = lon1 - np.arctan2(
        sinazimuth_equator * np.sin(great_circle_equator), np.cos(great_circle_equator)
    )
    # The great-circle distance between start and end (in radians)
    # This is the haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
    great_circle_distance = 2 * np.arcsin(
        np.sqrt(
            np.sin((lat2 - lat1) / 2) ** 2
            + coslat1 * coslat2 * np.sin((lon2 - lon1) / 2) ** 2
        )
    )
    # Generate evenly spaced points along the great circle.
    # Multiply by the radius so the distance is compatible with the spacing but
    # divide after because calculations below are for unit radius.
    distances = (
        line_coordinates(
            0,
            great_circle_distance * radius,
            size=size,
            spacing=spacing,
            adjust="spacing",
        )
        / radius
    )
    # Make the distances relative to where the great circle cross the equator
    # This is needed for the calculations below.
    distances_equator = distances + great_circle_equator
    sindistances_equator = np.sin(distances_equator)
    cosdistances_equator = np.cos(distances_equator)
    # Calculate the lon/lat coordinates of each point given their arc distance
    # and the azimuth of the great circle
    latitudes = np.degrees(
        np.arctan2(
            cosazimuth_equator * sindistances_equator,
            np.sqrt(
                cosdistances_equator**2
                + (sinazimuth_equator * sindistances_equator) ** 2
            ),
        )
    )
    longitudes = np.degrees(
        lon_equator
        + np.arctan2(sinazimuth_equator * sindistances_equator, cosdistances_equator)
    )
    coordinates = [longitudes, latitudes]
    if non_dimensional_coords is not None:
        for value in np.atleast_1d(non_dimensional_coords):
            coordinates.append(np.full_like(coordinates[0], value))
    # Convert the arc-distances into meters
    distances *= radius
    return tuple(coordinates), distances
