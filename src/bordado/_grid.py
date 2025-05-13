# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Generate coordinates for regular n-dimensional grids.
"""

import numpy as np

from ._line import line_coordinates
from ._validation import check_region, check_shape


def grid_coordinates(
    region,
    *,
    shape=None,
    spacing=None,
    adjust="spacing",
    pixel_register=False,
    non_dimensional_coords=None,
):
    """
    Generate evenly spaced points on an n-dimensional grid.

    The grid can be specified by either the number of points in each dimension
    (the *shape*) or by the grid node *spacing* in each dimension.

    If the given region is not divisible by the desired spacing, either the
    region or the spacing will have to be adjusted. By default, the spacing
    will be rounded to the nearest multiple. Optionally, the boundaries of the
    region can be adjusted to fit the exact spacing given. See the examples
    below.

    Supports laying out points on a grid-node registration or a pixel
    registration. See examples below for more information.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.
    shape : tuple = (..., size_SN, size_WE) or None
        The number of points in each direction of the given region, in reverse
        order. Must have one integer value per dimension of the region. The
        order of arguments is the opposite of the order of the region for
        compatibility with numpy's ``.shape`` attribute. If None, *spacing*
        must be provided. Default is None.
    spacing : float, tuple = (..., space_SN, space_WE), or None
        The grid spacing in each direction of the given region, in reverse
        order. A single value means that the spacing is equal in all
        directions. If a tuple, must have one value per dimension of the
        region. The order of arguments is the opposite of the order of the
        region for compatibility with *shape*. If None, *shape* must be
        provided. Default is None.
    adjust : str = "spacing" or "region"
        Whether to adjust the spacing or the region if the spacing is not
        a multiple of the region. Ignored if *shape* is given instead of
        *spacing*. Default is ``"spacing"``.
    pixel_register : bool
        If True, the coordinates will refer to the center of each grid pixel
        instead of the grid lines. In practice, this means that there will be
        one less element per dimension of the grid when compared to grid line
        registered (only if given *spacing* and not *shape*). Default is False.
    non_dimensional_coords : None, scalar, or tuple of scalars
        If not None, then value(s) of extra non-dimensional coordinates
        (coordinates that aren't part of the grid dimensions, like height for
        a lat/lon grid). Will generate extra coordinate arrays from these
        values with the same shape of the final grid coordinates and the
        constant value given here. Use this to generate arrays of constant
        heights or times, for example, which might be needed to accompany
        a grid.

    Returns
    -------
    coordinates : tuple of arrays
        Arrays with coordinates of each point in the grid. Each array contains
        values for a dimension in the order of the given region, and any extra
        values given in *non_dimensional_coords*. All arrays will have the same
        shape.

    Examples
    --------
    >>> east, north = grid_coordinates(region=(0, 5, 0, 10), shape=(5, 3))
    >>> print(east.shape, north.shape)
    (5, 3) (5, 3)
    >>> print(east)
    [[0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]]
    >>> print(north)
    [[ 0.   0.   0. ]
     [ 2.5  2.5  2.5]
     [ 5.   5.   5. ]
     [ 7.5  7.5  7.5]
     [10.  10.  10. ]]

    The grid can also be specified using the spacing between points instead of
    the shape:

    >>> east, north = grid_coordinates(region=(0, 5, 0, 10), spacing=2.5)
    >>> print(east.shape, north.shape)
    (5, 3) (5, 3)
    >>> print(east)
    [[0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]
     [0.  2.5 5. ]]
    >>> print(north)
    [[ 0.   0.   0. ]
     [ 2.5  2.5  2.5]
     [ 5.   5.   5. ]
     [ 7.5  7.5  7.5]
     [10.  10.  10. ]]

    The spacing can be different for northing and easting, respectively:

    >>> east, north = grid_coordinates(region=(-5, 1, 0, 10), spacing=(2.5, 1))
    >>> print(east.shape, north.shape)
    (5, 7) (5, 7)
    >>> print(east)
    [[-5. -4. -3. -2. -1.  0.  1.]
     [-5. -4. -3. -2. -1.  0.  1.]
     [-5. -4. -3. -2. -1.  0.  1.]
     [-5. -4. -3. -2. -1.  0.  1.]
     [-5. -4. -3. -2. -1.  0.  1.]]
    >>> print(north)
    [[ 0.   0.   0.   0.   0.   0.   0. ]
     [ 2.5  2.5  2.5  2.5  2.5  2.5  2.5]
     [ 5.   5.   5.   5.   5.   5.   5. ]
     [ 7.5  7.5  7.5  7.5  7.5  7.5  7.5]
     [10.  10.  10.  10.  10.  10.  10. ]]

    Grids of more dimensions can be generated by specifying more elements in
    ``region`` and ``shape``/``spacing``:

    >>> east, north, up = grid_coordinates(
    ...     region=(0, 5, 0, 10, -4, 0), shape=(2, 5, 3)
    ... )
    >>> print(east.shape, north.shape, up.shape)
    (2, 5, 3) (2, 5, 3) (2, 5, 3)
    >>> print(east)
    [[[0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]]
    <BLANKLINE>
     [[0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]
      [0.  2.5 5. ]]]
    >>> print(north)
    [[[ 0.   0.   0. ]
      [ 2.5  2.5  2.5]
      [ 5.   5.   5. ]
      [ 7.5  7.5  7.5]
      [10.  10.  10. ]]
    <BLANKLINE>
     [[ 0.   0.   0. ]
      [ 2.5  2.5  2.5]
      [ 5.   5.   5. ]
      [ 7.5  7.5  7.5]
      [10.  10.  10. ]]]
    >>> print(up)
    [[[-4. -4. -4.]
      [-4. -4. -4.]
      [-4. -4. -4.]
      [-4. -4. -4.]
      [-4. -4. -4.]]
    <BLANKLINE>
     [[ 0.  0.  0.]
      [ 0.  0.  0.]
      [ 0.  0.  0.]
      [ 0.  0.  0.]
      [ 0.  0.  0.]]]

    If the region can't be divided into the desired spacing, the spacing will
    be adjusted to conform to the region:

    >>> east, north = grid_coordinates(region=(-5, 0, 0, 5), spacing=2.6)
    >>> print(east.shape, north.shape)
    (3, 3) (3, 3)
    >>> print(east)
    [[-5.  -2.5  0. ]
     [-5.  -2.5  0. ]
     [-5.  -2.5  0. ]]
    >>> print(north)
    [[0.  0.  0. ]
     [2.5 2.5 2.5]
     [5.  5.  5. ]]
    >>> east, north = grid_coordinates(region=(-5, 0, 0, 5), spacing=2.4)
    >>> print(east.shape, north.shape)
    (3, 3) (3, 3)
    >>> print(east)
    [[-5.  -2.5  0. ]
     [-5.  -2.5  0. ]
     [-5.  -2.5  0. ]]
    >>> print(north)
    [[0.  0.  0. ]
     [2.5 2.5 2.5]
     [5.  5.  5. ]]

    You can choose to adjust the East and North boundaries of the region
    instead:

    >>> east, north = grid_coordinates(
    ...     region=(-5, 0, 0, 5), spacing=2.6, adjust='region',
    ... )
    >>> print(east.shape, north.shape)
    (3, 3) (3, 3)
    >>> print(east)
    [[-5.1 -2.5  0.1]
     [-5.1 -2.5  0.1]
     [-5.1 -2.5  0.1]]
    >>> print(north)
    [[-0.1 -0.1 -0.1]
     [ 2.5  2.5  2.5]
     [ 5.1  5.1  5.1]]
    >>> east, north = grid_coordinates(
    ...     region=(-5, 0, 0, 5), spacing=2.4, adjust='region',
    ... )
    >>> print(east.shape, north.shape)
    (3, 3) (3, 3)
    >>> print(east)
    [[-4.9 -2.5 -0.1]
     [-4.9 -2.5 -0.1]
     [-4.9 -2.5 -0.1]]
    >>> print(north)
    [[0.1 0.1 0.1]
     [2.5 2.5 2.5]
     [4.9 4.9 4.9]]

    We can optionally generate coordinates for the center of each grid pixel
    instead of the corner (default):

    >>> east, north = grid_coordinates(
    ...     region=(0, 5, 0, 10), spacing=2.5, pixel_register=True,
    ... )
    >>> # Notice that the shape is 1 less than when pixel_register=False
    >>> print(east.shape, north.shape)
    (4, 2) (4, 2)
    >>> print(east)
    [[1.25 3.75]
     [1.25 3.75]
     [1.25 3.75]
     [1.25 3.75]]
    >>> print(north)
    [[1.25 1.25]
     [3.75 3.75]
     [6.25 6.25]
     [8.75 8.75]]
    >>> east, north = grid_coordinates(
    ...     region=(0, 5, 0, 10), shape=(4, 2), pixel_register=True,
    ... )
    >>> print(east)
    [[1.25 3.75]
     [1.25 3.75]
     [1.25 3.75]
     [1.25 3.75]]
    >>> print(north)
    [[1.25 1.25]
     [3.75 3.75]
     [6.25 6.25]
     [8.75 8.75]]

    Generate arrays for other coordinates that have a constant value:

    >>> east, north, height = grid_coordinates(
    ...     region=(0, 5, 0, 10), spacing=2.5, non_dimensional_coords=57
    ... )
    >>> print(east.shape, north.shape, height.shape)
    (5, 3) (5, 3) (5, 3)
    >>> print(height)
    [[57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]]
    >>> east, north, height, time = grid_coordinates(
    ...     region=(0, 5, 0, 10), spacing=2.5, non_dimensional_coords=[57, 0.1]
    ... )
    >>> print(east.shape, north.shape, height.shape, time.shape)
    (5, 3) (5, 3) (5, 3) (5, 3)
    >>> print(height)
    [[57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]
     [57. 57. 57.]]
    >>> print(time)
    [[0.1 0.1 0.1]
     [0.1 0.1 0.1]
     [0.1 0.1 0.1]
     [0.1 0.1 0.1]
     [0.1 0.1 0.1]]

    """
    check_region(region)
    ndims = len(region) // 2
    if shape is not None and spacing is not None:
        message = (
            f"Both grid shape ('{shape}') and spacing ('{spacing}') were provided. "
            "Only one is allowed."
        )
        raise ValueError(message)
    if shape is None and spacing is None:
        message = "Either a grid shape or a spacing must be provided."
        raise ValueError(message)
    if shape is None:
        shape = tuple(None for _ in range(ndims))
        if np.isscalar(spacing):
            spacing = tuple(spacing for _ in range(ndims))
        elif len(spacing) != ndims:
            message = (
                f"Invalid spacing '{spacing}'. Should have {ndims} values, "
                f"one value per dimension of the region '{region}'."
            )
            raise ValueError(message)
    else:
        spacing = tuple(None for _ in range(ndims))
    # Must check the shape after so that it's guaranteed to be a tuple.
    check_shape(shape, region)
    region_pairs = np.reshape(region, (len(region) // 2, 2))
    coordinates_1d = []
    for size, space, (low, up) in zip(reversed(shape), reversed(spacing), region_pairs):
        coordinates_1d.append(
            line_coordinates(
                low,
                up,
                size=size,
                spacing=space,
                adjust=adjust,
                pixel_register=pixel_register,
            )
        )
    # Use the ij indexing in meshgrid because the default xy works for 2D
    # arrays fine but mixes the order of coordinates for 3D and beyond. But
    # this means we have to reverse the list going in to get the right shape
    # and reverse it coming out to get the right order of coordinates.
    coordinates = list(reversed(np.meshgrid(*reversed(coordinates_1d), indexing="ij")))
    if non_dimensional_coords is not None:
        for value in np.atleast_1d(non_dimensional_coords):
            coordinates.append(np.full_like(coordinates[0], value))
    return tuple(coordinates)
