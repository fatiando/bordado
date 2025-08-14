# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for generating random point spreads.
"""

import numpy as np

from ._utils import make_non_dimensional_coordinates
from ._validation import check_region, check_region_geographic, longitude_continuity


def random_coordinates(region, size, *, random_seed=None, non_dimensional_coords=None):
    """
    Generate the coordinates for a uniformly random scatter of points.

    The points are drawn from a uniform distribution, independently for each
    dimension of the given region.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.
    size : int
        The number of points to generate.
    random_seed : None or int or numpy.random.Generator
        A seed for a random number generator (RNG) used to generate the
        coordinates. If an integer is given, it will be used as a seed for
        :func:`numpy.random.default_rng` which will then be used as the
        generator. If a :class:`numpy.random.Generator` is given, it will be
        used. If ``None`` is given, :func:`~numpy.random.default_rng` will be
        used with no seed to create a generator (resulting in different numbers
        with each run). Use a seed to make sure computations are reproducible.
        Default is None.
    non_dimensional_coords : None, scalar, or tuple of scalars
        If not None, then value(s) of extra non-dimensional coordinates
        (coordinates that aren't part of the sample dimensions, like height for
        a lat/lon grid). Will generate extra coordinate arrays from these
        values with the same shape of the final coordinates and the constant
        value given here. Use this to generate arrays of constant heights or
        times, for example, which might be needed to accompany a set of points.

    Returns
    -------
    coordinates : tuple of arrays
        Arrays with coordinates of each point in the grid. Each array contains
        values for a dimension in an order compatible with *region* followed by
        any extra dimensions given in *non_dimensional_coords*. All arrays will
        have the specified *size*.

    Examples
    --------
    We'll use a seed value to ensure that the same will be generated every
    time:

    >>> easting, northing = random_coordinates(
    ...     (0, 10, -2, -1), size=4, random_seed=0,
    ... )
    >>> print(', '.join(['{:.4f}'.format(i) for i in easting]))
    6.3696, 2.6979, 0.4097, 0.1653
    >>> print(', '.join(['{:.4f}'.format(i) for i in northing]))
    -1.1867, -1.0872, -1.3934, -1.2705
    >>> easting, northing, height = random_coordinates(
    ...     (0, 10, -2, -1), 4, random_seed=0, non_dimensional_coords=12
    ... )
    >>> print(height)
    [12. 12. 12. 12.]
    >>> easting, northing, height, time = random_coordinates(
    ...     (0, 10, -2, -1),
    ...     size=4,
    ...     random_seed=0,
    ...     non_dimensional_coords=[12, 1986],
    ... )
    >>> print(height)
    [12. 12. 12. 12.]
    >>> print(time)
    [1986. 1986. 1986. 1986.]

    We're not limited to 2 dimensions:

    >>> easting, northing, up = random_coordinates(
    ...     (0, 10, -2, -1, 0.1, 0.2), 4, random_seed=0,
    ... )
    >>> print(', '.join(['{:.4f}'.format(i) for i in easting]))
    6.3696, 2.6979, 0.4097, 0.1653
    >>> print(', '.join(['{:.4f}'.format(i) for i in northing]))
    -1.1867, -1.0872, -1.3934, -1.2705
    >>> print(', '.join(['{:.4f}'.format(i) for i in up]))
    0.1544, 0.1935, 0.1816, 0.1003

    """
    check_region(region)
    random = np.random.default_rng(random_seed)
    coordinates = []
    for lower, upper in np.reshape(region, (len(region) // 2, 2)):
        coordinates.append(random.uniform(lower, upper, size))
    coordinates.extend(
        make_non_dimensional_coordinates(
            non_dimensional_coords, coordinates[0].shape, coordinates[0].dtype
        )
    )
    return tuple(coordinates)


def random_coordinates_spherical(
    region, size, *, random_seed=None, non_dimensional_coords=None
):
    """
    Generate the coordinates for uniformly random points on the sphere.

    Points drawn from a simple uniform distribution of longitude and latitude
    will tend to be more concentrated towards the poles. This function accounts
    for that and is able generate a uniformly random distribution on the
    surface of a sphere.

    Parameters
    ----------
    region : tuple = (W, E, S, N)
        The boundaries of a given region in geographic coordinates. Should have
        a lower and an upper boundary for each dimension of the coordinate
        system.
    size : int
        The number of points to generate.
    random_seed : None or int or numpy.random.Generator
        A seed for a random number generator (RNG) used to generate the
        coordinates. If an integer is given, it will be used as a seed for
        :func:`numpy.random.default_rng` which will then be used as the
        generator. If a :class:`numpy.random.Generator` is given, it will be
        used. If ``None`` is given, :func:`~numpy.random.default_rng` will be
        used with no seed to create a generator (resulting in different numbers
        with each run). Use a seed to make sure computations are reproducible.
        Default is None.
    non_dimensional_coords : None, scalar, or tuple of scalars
        If not None, then value(s) of extra non-dimensional coordinates
        (coordinates that aren't part of the sample dimensions, like height for
        a lat/lon grid). Will generate extra coordinate arrays from these
        values with the same shape of the final coordinates and the constant
        value given here. Use this to generate arrays of constant heights or
        times, for example, which might be needed to accompany a set of points.

    Returns
    -------
    coordinates : tuple of arrays
        Arrays with the longitude, latitude, and non-dimensional coordinates,
        in order, of each point in the grid. Each array contains values for
        a dimension in an order compatible with *region* followed by any extra
        dimensions given in *non_dimensional_coords*. All arrays will have the
        specified *size*.

    Examples
    --------
    We can generate the random coordinates on a sphere like so:

    >>> coordinates = random_coordinates_spherical(
    ...     region=(-100, 100, -80, -20), size=10, random_seed=42,
    ... )

    We set a seed here to make sure our examples always return the same values.
    If you need different values every time you run your code, then either omit
    ``random_seed`` or set it to ``None``.

    >>> import numpy as np

    The first coordinate is the longitude:

    >>> print(np.array_str(coordinates[0], precision=1))
    [ 54.8 -12.2  71.7  39.5 -81.2  95.1  52.2  57.2 -74.4  -9.9]

    And the second is the latitude:

    >>> print(np.array_str(coordinates[1], precision=1))
    [-48.3 -22.9 -34.8 -27.1 -44.4 -57.  -38.9 -70.7 -26.9 -35.4]

    To show how this differs from :func:`bordado.random_coordinates`, we can
    generate a large number of points and calculate the point density per
    latitude band. We expect the concentration to be uniform since we want
    uniformly distributed numbers.

    First, we'll define a function that calculates the point density per 10
    degree band of latitude:

    >>> import bordado as bd
    >>> def point_density(coordinates, region):
    ...     # Define the latitude bands
    ...     bands = bd.line_coordinates(*region[2:], spacing=10)
    ...     # Calculate the area of each band.
    ...     # See https://en.wikipedia.org/wiki/Spherical_cap
    ...     areas = 2 * np.pi * abs(
    ...         np.sin(np.radians(bands[:-1])) - np.sin(np.radians(bands[1:]))
    ...     )
    ...     # Figure out how many points are in each band
    ...     points_per_band = np.array([
    ...         bd.inside(
    ...             coordinates,
    ...             [*region[:2], bands[i], bands[i + 1]],
    ...         ).sum()
    ...         for i in range(bands.size - 1)
    ...     ])
    ...     # Calculate the density
    ...     density = points_per_band / areas
    ...     return density

    Now we can make a lot of random points using this function and the
    traditional :func:`bordado.random_coordinates` to compare:

    >>> region = (0, 360, -90, 90)
    >>> size = 100_000
    >>> coordinates_cartesian = random_coordinates(
    ...     region, size, random_seed=42,
    ... )
    >>> coordinates_spherical = random_coordinates_spherical(
    ...     region, size, random_seed=42,
    ... )

    Finally, we calculate and print the point density per latitude for each
    set:

    >>> density_cartesian = point_density(coordinates_cartesian, region)
    >>> print(np.array_str(density_cartesian, precision=0))
    [57147. 19812. 12159.  8981.  7267.  6107.  5574.  5320.  5151.  5033.
      5237.  5558.  6138.  7075.  8800. 11967. 19660. 58635.]

    >>> density_spherical = point_density(coordinates_spherical, region)
    >>> print(np.array_str(density_spherical, precision=0))
    [8192. 7786. 7683. 8134. 8113. 8112. 7867. 7982. 8029. 7945. 7834. 7901.
     7931. 7902. 7924. 8037. 7987. 8119.]

    As you can see, for the Cartesian version the density increases towards the
    poles but for the spherical version it stays roughly the same throughout
    the globe.
    """
    check_region_geographic(region)
    region = longitude_continuity(region)
    random = np.random.default_rng(random_seed)
    colat_south = np.radians(90 - region[2])
    colat_north = np.radians(90 - region[3])
    xmax = (1 + np.cos(colat_north)) / 2
    xmin = (1 + np.cos(colat_south)) / 2
    coordinates = [
        random.uniform(*region[:2], size),
        90 - np.degrees(np.arccos(2 * random.uniform(xmin, xmax, size) - 1)),
    ]
    coordinates.extend(
        make_non_dimensional_coordinates(
            non_dimensional_coords, coordinates[0].shape, coordinates[0].dtype
        )
    )
    return tuple(coordinates)
