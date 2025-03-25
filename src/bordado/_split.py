# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions to split points into blocks and windows.
"""

import numpy as np
from scipy.spatial import KDTree

from ._coordinates import check_coordinates
from ._grid import grid_coordinates
from ._line import check_adjust
from ._region import check_region, get_region


def block_split(
    coordinates, *, region=None, block_shape=None, block_size=None, adjust="block_size"
):
    """
    Split a region into blocks and label points according to where they fall.

    The labels are integers corresponding to the index of the block. Also
    returns the coordinates of the center of each block (following the same
    index as the labels). Blocks can be specified by their size or the number
    of blocks in each dimension (the shape).

    Uses :class:`scipy.spatial.KDTree` to nearest neighbor lookup during the
    splitting process.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. The arrays can be
        n-dimensional.
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. If not region is given, will use the bounding region of
        the given coordinates.
    block_shape : tuple = (..., n_north, n_east) or None
        The number of blocks in each direction, in reverse order. Must have one
        integer value per coordinate dimension. The order of arguments is the
        opposite of the order of the region for compatibility with numpy's
        ``.shape`` attribute. If None, *block_size* must be provided. Default
        is None.
    block_size : float, tuple = (..., size_north, size_east), or None
        The block size in each direction, in reverse order. A single value
        means that the block size is equal in all directions. If a tuple, must
        have one value per dimension of the coordinates. The order of arguments
        is the opposite of the order of the coordinates for compatibility with
        *block_shape*. If None, *block_shape* must be provided. Default is
        None.
    adjust : str = "block_size" or "region"
        Whether to adjust the block size or the region, if required. Adjusting
        the size or region is required when the block size is not a multiple of
        the region. Ignored if *block_shape* is given instead of *block_size*.
        Defaults to adjusting the block size.

    Returns
    -------
    block_coordinates : tuple = (easting, northing, ...)
        ND arrays with the coordinates of the center of each block.
    labels : array
        Array with the same shape as the block coordinates. Contains the
        integer label for each data point. The label is the index of the block
        to which that point belongs.

    Examples
    --------
    Let's make some points along a 2D grid to try splitting (the points don't
    have to be on a grid but this makes it easier to explain):

    >>> import bordado as bd
    >>> coordinates = bd.grid_coordinates((-5, 0, 5, 10), spacing=1)
    >>> print(coordinates[0].shape)
    (6, 6)
    >>> print(coordinates[0])
    [[-5. -4. -3. -2. -1.  0.]
     [-5. -4. -3. -2. -1.  0.]
     [-5. -4. -3. -2. -1.  0.]
     [-5. -4. -3. -2. -1.  0.]
     [-5. -4. -3. -2. -1.  0.]
     [-5. -4. -3. -2. -1.  0.]]
    >>> print(coordinates[1])
    [[ 5.  5.  5.  5.  5.  5.]
     [ 6.  6.  6.  6.  6.  6.]
     [ 7.  7.  7.  7.  7.  7.]
     [ 8.  8.  8.  8.  8.  8.]
     [ 9.  9.  9.  9.  9.  9.]
     [10. 10. 10. 10. 10. 10.]]

    We can split into blocks by specifying the block size:

    >>> block_coords, labels = block_split(coordinates, block_size=2.5)

    The first argument is a tuple of coordinates for the center of each block:

    >>> print(len(block_coords))
    2
    >>> print(block_coords[0])
    [[-3.75 -1.25]
     [-3.75 -1.25]]
    >>> print(block_coords[1])
    [[6.25 6.25]
     [8.75 8.75]]

    The labels are an array of the same shape as the coordinates and has the
    index of the block each point belongs to:

    >>> print(labels)
    [[0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [2 2 2 3 3 3]
     [2 2 2 3 3 3]
     [2 2 2 3 3 3]]

    Use this to index the coordinates, for example to get all points that fall
    inside the first block:

    >>> block_0 = [c[labels == 0] for c in coordinates]
    >>> print(block_0[0])
    [-5. -4. -3. -5. -4. -3. -5. -4. -3.]
    >>> print(block_0[1])
    [5. 5. 5. 6. 6. 6. 7. 7. 7.]

    You can also specify the number of blocks along each direction instead of
    their size:

    >>> block_coords, labels = block_split(coordinates, block_shape=(4, 2))
    >>> print(len(block_coords))
    2
    >>> print(block_coords[0])
    [[-3.75 -1.25]
     [-3.75 -1.25]
     [-3.75 -1.25]
     [-3.75 -1.25]]
    >>> print(block_coords[1])
    [[5.625 5.625]
     [6.875 6.875]
     [8.125 8.125]
     [9.375 9.375]]
    >>> print(labels)
    [[0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [2 2 2 3 3 3]
     [4 4 4 5 5 5]
     [6 6 6 7 7 7]
     [6 6 6 7 7 7]]

    By default, the region (bounding box of the points) will be derived from
    the coordinates. You can also specify a custom region for the splitting if
    desired:

    >>> block_coords, labels = block_split(
    ...     coordinates, block_size=2, region=(-5.5, 0.5, 4.5, 10.5),
    ... )
    >>> print(block_coords[0])
    [[-4.5 -2.5 -0.5]
     [-4.5 -2.5 -0.5]
     [-4.5 -2.5 -0.5]]
    >>> print(block_coords[1])
    [[5.5 5.5 5.5]
     [7.5 7.5 7.5]
     [9.5 9.5 9.5]]
    >>> print(labels)
    [[0 0 1 1 2 2]
     [0 0 1 1 2 2]
     [3 3 4 4 5 5]
     [3 3 4 4 5 5]
     [6 6 7 7 8 8]
     [6 6 7 7 8 8]]

    Coordinates can be more than 2-dimensional as well:

    >>> coordinates = bd.grid_coordinates((-5, 0, 5, 10, 1, 2), spacing=1)
    >>> print(coordinates[0].shape)
    (2, 6, 6)
    >>> print(coordinates[0])
    [[[-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]]
    <BLANKLINE>
     [[-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]
      [-5. -4. -3. -2. -1.  0.]]]
    >>> print(coordinates[1])
    [[[ 5.  5.  5.  5.  5.  5.]
      [ 6.  6.  6.  6.  6.  6.]
      [ 7.  7.  7.  7.  7.  7.]
      [ 8.  8.  8.  8.  8.  8.]
      [ 9.  9.  9.  9.  9.  9.]
      [10. 10. 10. 10. 10. 10.]]
    <BLANKLINE>
     [[ 5.  5.  5.  5.  5.  5.]
      [ 6.  6.  6.  6.  6.  6.]
      [ 7.  7.  7.  7.  7.  7.]
      [ 8.  8.  8.  8.  8.  8.]
      [ 9.  9.  9.  9.  9.  9.]
      [10. 10. 10. 10. 10. 10.]]]
    >>> print(coordinates[2])
    [[[1. 1. 1. 1. 1. 1.]
      [1. 1. 1. 1. 1. 1.]
      [1. 1. 1. 1. 1. 1.]
      [1. 1. 1. 1. 1. 1.]
      [1. 1. 1. 1. 1. 1.]
      [1. 1. 1. 1. 1. 1.]]
    <BLANKLINE>
     [[2. 2. 2. 2. 2. 2.]
      [2. 2. 2. 2. 2. 2.]
      [2. 2. 2. 2. 2. 2.]
      [2. 2. 2. 2. 2. 2.]
      [2. 2. 2. 2. 2. 2.]
      [2. 2. 2. 2. 2. 2.]]]
    >>> block_coords, labels = block_split(
    ...     coordinates, block_size=2.5, adjust="region",
    ... )
    >>> print(labels)
    [[[0 0 0 1 1 1]
      [0 0 0 1 1 1]
      [0 0 0 1 1 1]
      [2 2 2 3 3 3]
      [2 2 2 3 3 3]
      [2 2 2 3 3 3]]
    <BLANKLINE>
     [[0 0 0 1 1 1]
      [0 0 0 1 1 1]
      [0 0 0 1 1 1]
      [2 2 2 3 3 3]
      [2 2 2 3 3 3]
      [2 2 2 3 3 3]]]

    """
    coordinates = check_coordinates(coordinates)
    adjust_translation = {"block_size": "spacing", "region": "region"}
    check_adjust(adjust, valid=adjust_translation.keys())
    if region is None:
        region = get_region(coordinates)
    else:
        check_region(region)
    block_coordinates = grid_coordinates(
        region,
        spacing=block_size,
        shape=block_shape,
        adjust=adjust_translation[adjust],
        pixel_register=True,
    )
    tree = KDTree(np.transpose([c.ravel() for c in block_coordinates]))
    labels = tree.query(np.transpose([c.ravel() for c in coordinates]))[1]
    return block_coordinates, labels.reshape(coordinates[0].shape)
