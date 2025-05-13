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

from ._grid import grid_coordinates
from ._region import get_region, pad_region
from ._validation import check_adjust, check_coordinates, check_region


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
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape.
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. If region is not given, will use the bounding region of
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


def rolling_window(coordinates, window_size, overlap, *, region=None, adjust="overlap"):
    """
    Split points into overlapping windows.

    A window of the given size is moved across the region at a given step
    (specified by *spacing* or *shape*). Returns the indices of points falling
    inside each window step. You can use the indices to select points falling
    inside a given window.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape.
    window_size : float
        The size of the windows. Units should match the units of *coordinates*.
        In case the window size is not a multiple of the region, either of them
        will be adjusted according to the value of the *adjust* argument.
    overlap : float
        The amount of overlap between adjacent windows. Should be within the
        range 1 > overlap ≥ 0. For example, an overlap of 0.5 means 50%
        overlap. An overlap of 0 will be the same as
        :func:`~bordado.block_split`.
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. If region is not given, will use the bounding region of
        the given coordinates.
    adjust : str = "overlap" or "region"
        Whether to adjust the window overlap or the region, if required.
        Adjusting the overlap or region is required when the combination of
        window size and overlap is not a multiple of the region. Defaults to
        adjusting the overlap.

    Returns
    -------
    window_coordinates : tuple = (easting, northing, ...)
        ND coordinate arrays for the center of each window. Will have the same
        number of arrays as the *coordinates* and each array will have the
        number of dimensions equal to ``len(coordinates)``.
    indices : array
        An array with the same shape as the *window_coordinates*. Each element
        of the array is a tuple of arrays (with the same length as
        *coordinates*) corresponding to the indices of the points that fall
        inside that particular window. Use these indices to index the given
        *coordinates* and select points from a window.

    Examples
    --------
    Generate a set of sample coordinates on a grid to make it easier to
    visualize the windows:

    >>> import bordado as bd
    >>> coordinates = bd.grid_coordinates((-5, -1, 6, 10), spacing=1)
    >>> print(coordinates[0])
    [[-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]]
    >>> print(coordinates[1])
    [[ 6.  6.  6.  6.  6.]
     [ 7.  7.  7.  7.  7.]
     [ 8.  8.  8.  8.  8.]
     [ 9.  9.  9.  9.  9.]
     [10. 10. 10. 10. 10.]]

    Get the coordinates of the centers of rolling windows with 75% overlap and
    an indexer that allows us to select points from each window:

    >>> window_coords, indices = rolling_window(
    ...     coordinates, window_size=2, overlap=0.75,
    ... )

    Window coordinates will be 2D arrays. Their shape is the number of windows
    in each dimension:

    >>> print(window_coords[0].shape, window_coords[1].shape)
    (5, 5) (5, 5)

    The values of these arrays are the coordinates for the center of each
    rolling window:

    >>> print(window_coords[0])
    [[-4.  -3.5 -3.  -2.5 -2. ]
     [-4.  -3.5 -3.  -2.5 -2. ]
     [-4.  -3.5 -3.  -2.5 -2. ]
     [-4.  -3.5 -3.  -2.5 -2. ]
     [-4.  -3.5 -3.  -2.5 -2. ]]
    >>> print(window_coords[1])
    [[7.  7.  7.  7.  7. ]
     [7.5 7.5 7.5 7.5 7.5]
     [8.  8.  8.  8.  8. ]
     [8.5 8.5 8.5 8.5 8.5]
     [9.  9.  9.  9.  9. ]]

    The indices of points falling on each window will have the same shape as
    the window center coordinates:

    >>> print(indices.shape)
    (5, 5)

    Each element of the indices array is a tuple of arrays, one for each
    element in the ``coordinates``:

    >>> print(len(indices[0, 0]))
    2

    They are indices of the points that fall inside the selected window. The
    first element indexes the axis 0 of the coordinate arrays and so forth:

    >>> print(indices[0, 0][0])
    [0 0 0 1 1 1 2 2 2]
    >>> print(indices[0, 0][1])
    [0 1 2 0 1 2 0 1 2]
    >>> print(indices[0, 1][0])
    [0 0 1 1 2 2]
    >>> print(indices[0, 1][1])
    [1 2 1 2 1 2]
    >>> print(indices[0, 2][0])
    [0 0 0 1 1 1 2 2 2]
    >>> print(indices[0, 2][1])
    [1 2 3 1 2 3 1 2 3]

    Use these indices to select the coordinates the points that fall inside
    a window:

    >>> points_window_00 = [c[indices[0, 0]] for c in coordinates]
    >>> print(points_window_00[0])
    [-5. -4. -3. -5. -4. -3. -5. -4. -3.]
    >>> print(points_window_00[1])
    [6. 6. 6. 7. 7. 7. 8. 8. 8.]
    >>> points_window_01 = [c[indices[0, 1]] for c in coordinates]
    >>> print(points_window_01[0])
    [-4. -3. -4. -3. -4. -3.]
    >>> print(points_window_01[1])
    [6. 6. 7. 7. 8. 8.]

    If the coordinates are 1D, the indices will also be 1D:

    >>> coordinates1d = [c.ravel() for c in coordinates]
    >>> window_coords, indices = rolling_window(
    ...     coordinates1d, window_size=2, overlap=0.75,
    ... )
    >>> print(len(indices[0, 0]))
    1
    >>> print(indices[0, 0][0])
    [ 0  1  2  5  6  7 10 11 12]
    >>> print(indices[0, 1][0])
    [ 1  2  6  7 11 12]

    The returned indices can be used in the same way as before to get the same
    coordinates:

    >>> print(coordinates1d[0][indices[0, 0]])
    [-5. -4. -3. -5. -4. -3. -5. -4. -3.]
    >>> print(coordinates1d[1][indices[0, 0]])
    [6. 6. 6. 7. 7. 7. 8. 8. 8.]

    By default, the windows will span the entire data region. You can also
    control the specific region you'd like the windows to cover:

    >>> coordinates = grid_coordinates((-10, 5, 0, 20), spacing=1)
    >>> window_coords, indices = rolling_window(
    ...     coordinates, window_size=2, overlap=0.75, region=(-5, -1, 6, 10),
    ... )

    Even though the data region is larger, our rolling windows should still be
    the same as before:

    >>> print(coordinates[0][indices[0, 1]])
    [-4. -3. -4. -3. -4. -3.]
    >>> print(coordinates[1][indices[0, 1]])
    [6. 6. 7. 7. 8. 8.]

    """
    coordinates = check_coordinates(coordinates)
    adjust_translation = {"overlap": "spacing", "region": "region"}
    check_adjust(adjust, valid=adjust_translation.keys())
    if region is None:
        region = get_region(coordinates)
    else:
        check_region(region)
    # Check if window size is bigger than the minimum dimension of the region
    if window_size > min(region[1] - region[0], region[3] - region[2]):
        message = (
            f"Invalid window size '{window_size}'. Cannot be larger than dimensions of "
            f"the region '{region}'."
        )
        raise ValueError(message)
    # Check that the overlap is valid. It should be a percentage < 100%.
    if overlap < 0 or overlap >= 1:
        message = f"Invalid overlap '{overlap}'. Must be 1 > overlap >= 0."
        raise ValueError(message)
    # Calculate the region spanning the centers of the rolling windows
    window_region = pad_region(region, -window_size / 2)
    # Calculate the window step based on the amount of overlap
    window_step = (1 - overlap) * window_size
    # Get the coordinates of the centers of each window
    centers = grid_coordinates(
        window_region, spacing=window_step, adjust=adjust_translation[adjust]
    )
    # Use a KD-tree to get the neighbords that fall within half a window size
    # of the window centers.
    tree = KDTree(np.transpose([c.ravel() for c in coordinates]))
    # Coordinates must be transposed because the kd-tree wants them as columns
    # of a matrix. Use p=inf (infinity norm) to get square windows instead of
    # circular ones.
    indices1d = tree.query_ball_point(
        np.transpose([c.ravel() for c in centers]), r=window_size / 2, p=np.inf
    )
    # Make the indices array the same shape as the center coordinates array.
    # That preserves the information of the number of windows in each
    # dimension. Need to first create an empty array of object type because
    # otherwise numpy tries to use the index tuples as dimensions (even if
    # given ndim=1 explicitly). Can't make it 1D and then reshape because the
    # reshape is ignored for some reason. The workaround is to create the array
    # with the correct shape and assign the values to a raveled view of the
    # array.
    indices = np.empty(centers[0].shape, dtype="object")
    # Need to convert the indices to int arrays because unravel_index doesn't
    # like empty lists but can handle empty integer arrays in case a window has
    # no points inside it.
    indices.ravel()[:] = [
        np.unravel_index(np.array(i, dtype="int"), shape=coordinates[0].shape)
        for i in indices1d
    ]
    return centers, indices


def expanding_window(coordinates, center, sizes):
    """
    Select points on windows of expanding size around a center point.

    Produces arrays for indexing the given coordinates to obtain points falling
    inside each window (see examples below). The windows do not necessarily
    have to be expanding in size (the sizes can be in any order).

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists or any numpy-compatible array type. Arrays can be of any
        shape but must all have the same shape.
    center : tuple = (easting, northing, ...)
        The coordinates of the center of the window. Must have the same number
        of elements as *coordinates*. Coordinates **cannot be arrays**.
    sizes : array
        The sizes of the windows. Does not have to be in any particular order.
        The order of indices returned will match the order of window sizes
        given. Units should match the units of *coordinates* and *center*.

    Returns
    -------
    indices : list
        Each element of the list corresponds to the indices of points falling
        inside a window. Use them to index the coordinates for each window. The
        indices will depend on the number of dimensions in the input
        coordinates. For example, if the coordinates are 2D arrays, each window
        will contain indices for 2 dimensions (row, column).

    Examples
    --------
    Generate a set of sample coordinates on a grid to make it easier to
    visualize:

    >>> import bordado as bd
    >>> coordinates = bd.grid_coordinates((-5, -1, 6, 10), spacing=1)
    >>> print(coordinates[0])
    [[-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]
     [-5. -4. -3. -2. -1.]]
    >>> print(coordinates[1])
    [[ 6.  6.  6.  6.  6.]
     [ 7.  7.  7.  7.  7.]
     [ 8.  8.  8.  8.  8.]
     [ 9.  9.  9.  9.  9.]
     [10. 10. 10. 10. 10.]]

    Get the expanding window indices (there should be one index per window):

    >>> indices = expanding_window(coordinates, center=(-3, 8), sizes=[1, 2])
    >>> print(len(indices))
    2

    Each element of the indices is a tuple with the arrays that index the
    coordinates that fall inside each window. For example, this is the index of
    the first window (with size 1):

    >>> print(len(indices[0]))
    2
    >>> print(indices[0][0], indices[0][1])
    [2] [2]

    The index have 2 values because the coordinate arrays are 2D, so we need an
    index of the rows and of the columns. We can use them to select points from
    the coordinates that fall inside the first window:

    >>> print(coordinates[0][indices[0]], coordinates[1][indices[0]])
    [-3.] [8.]

    For the other windows, it works the same:

    >>> for index in indices[1]:
    ...     print(index)
    [1 1 1 2 2 2 3 3 3]
    [1 2 3 1 2 3 1 2 3]
    >>> print(coordinates[0][indices[1]])
    [-4. -3. -2. -4. -3. -2. -4. -3. -2.]
    >>> print(coordinates[1][indices[1]])
    [7. 7. 7. 8. 8. 8. 9. 9. 9.]

    Let's make some 1D coordinates to show how this works in that case:

    >>> coordinates1d = tuple(c.ravel() for c in coordinates)

    Getting the indices is the same and there will still be 1 entry per window:

    >>> indices = expanding_window(coordinates1d, center=(-3, 8), sizes=[1, 2])
    >>> print(len(indices))
    2

    But since coordinates are 1D, there is only one index per window (it's
    still in a tuple, though):

    >>> print(len(indices[0]))
    1
    >>> print(indices[0][0])
    [12]

    >>> print(indices[1][0])
    [ 6  7  8 11 12 13 16 17 18]

    The returned indices can be used in the same way as before:

    >>> print(coordinates1d[0][indices[0]], coordinates1d[1][indices[0]])
    [-3.] [8.]

    Coordinates can be more than 2-dimensional as well:

    >>> coordinates3d = bd.grid_coordinates((-5, 0, 5, 10, 1, 2), spacing=1)
    >>> print(coordinates3d[0].shape)
    (2, 6, 6)
    >>> print(coordinates3d[0])
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
    >>> print(coordinates3d[1])
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
    >>> print(coordinates3d[2])
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

    The only difference is that the center coordinates also need to be in
    3-dimensional space (the size of the windows is uniform in all directions):

    >>> indices = expanding_window(
    ...     coordinates3d, center=(-2.5, 8.5, 1.5), sizes=[1, 2],
    ... )
    >>> print(len(indices))
    2

    Each index will have 3 elements, one for each dimension:

    >>> print(len(indices[0]))
    3
    >>> print(indices[0][0])
    [0 0 0 0 1 1 1 1]
    >>> print(indices[0][1])
    [3 3 4 4 3 3 4 4]
    >>> print(indices[0][2])
    [2 3 2 3 2 3 2 3]

    And extracting coordinates for each window also works the same:

    >>> print(coordinates3d[0][indices[0]])
    [-3. -2. -3. -2. -3. -2. -3. -2.]
    >>> print(coordinates3d[1][indices[0]])
    [8. 8. 9. 9. 8. 8. 9. 9.]
    >>> print(coordinates3d[2][indices[0]])
    [1. 1. 1. 1. 2. 2. 2. 2.]

    """
    coordinates = check_coordinates(coordinates)
    shape = coordinates[0].shape
    center = np.atleast_2d(center)
    tree = KDTree(np.transpose([c.ravel() for c in coordinates]))
    indices = []
    for size in sizes:
        # Use p=inf (infinity norm) to get square windows instead of circular
        index1d = tree.query_ball_point(center, r=size / 2, p=np.inf)[0]
        # Convert indices to an array to avoid errors when the index is empty
        # (no points in the window). unravel_index doesn't like empty lists.
        indices.append(np.unravel_index(np.array(index1d, dtype="int"), shape=shape))
    return indices
