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

from ._validation import check_region


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
    if non_dimensional_coords is not None:
        for value in np.atleast_1d(non_dimensional_coords):
            coordinates.append(np.full_like(coordinates[0], value))
    return tuple(coordinates)
