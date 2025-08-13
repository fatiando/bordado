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

from ._grid import grid_coordinates, line_coordinates
from ._region import get_region, pad_region
from ._validation import (
    check_adjust,
    check_coordinates,
    check_coordinates_geographic,
    check_overlap,
    check_region,
    check_region_geographic,
    longitude_continuity,
)


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
    (specified by the amount of overlap between adjacent windows). Returns the
    indices of points falling inside each window step. You can use the indices
    to select points falling inside a given window.

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
    check_overlap(overlap)
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


def rolling_window_spherical(coordinates, window_size, overlap, *, region=None):
    """
    Split points into overlapping equal area windows on the sphere.

    A window of the given latitudinal size is moved across the region at
    a given step (specified by the amount of overlap between adjacent windows).
    Windows are not regularly distributed on the sphere and are not "square" in
    longitude, latitude. They are evenly spaced in latitude but their
    longitudinal dimension varies to compensate for the convergence of
    meridians at the polar regions. The overlap will also wrap around the 360-0
    longitude discontinuity (see examples below).

    Returns the indices of points falling inside each window step. You can use
    the indices to select points falling inside a given window.

    Parameters
    ----------
    coordinates : tuple = (longitude, latitude)
        Tuple of arrays with the longitude and latitude coordinates of each
        point. Arrays can be Python lists or any numpy-compatible array type.
        Arrays can be of any shape but must all have the same shape.
    window_size : float
        The size of the windows along latitude in decimal degrees. The
        longitudinal window size is adjusted to retain equal area between
        windows. Must be > 0.
    overlap : float
        The amount of overlap between adjacent windows. Should be within the
        range 1 > overlap ≥ 0. For example, an overlap of 0.5 means 50%
        overlap. The overlap may have to be adjusted to make sure windows fit
        inside the given region exactly.
    region : tuple = (W, E, S, N)
        The boundaries of a given region in geographic coordinates. Should have
        a lower and an upper boundary for each dimension of the coordinate
        system. If region is not given, will use the bounding region of the
        given coordinates.

    Returns
    -------
    window_coordinates : tuple = (longitude, latitude)
        1D coordinate arrays for the center of each window.
    indices : array
        1D array with each element of the array being a tuple of 2 arrays
        corresponding to the indices of the points that fall inside that
        particular window. Use these indices to index the given *coordinates*
        and select points from a window.

    Notes
    -----
    Uses the method of [Malkin2016]_ to divide the region into overlapping
    windows of equal area. The windows will have the specified window size in
    latitude but their longitudinal dimensions will be adjusted to account for
    the convergence of meridians at the poles.

    Examples
    --------
    Generate a set of sample coordinates on a grid to make it easier to
    visualize the windows:

    >>> import bordado as bd
    >>> import numpy as np

    >>> coordinates = bd.grid_coordinates((0, 40, 60, 90), spacing=5)
    >>> print(coordinates[0])
    [[ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]
     [ 0.  5. 10. 15. 20. 25. 30. 35. 40.]]
    >>> print(coordinates[1])
    [[60. 60. 60. 60. 60. 60. 60. 60. 60.]
     [65. 65. 65. 65. 65. 65. 65. 65. 65.]
     [70. 70. 70. 70. 70. 70. 70. 70. 70.]
     [75. 75. 75. 75. 75. 75. 75. 75. 75.]
     [80. 80. 80. 80. 80. 80. 80. 80. 80.]
     [85. 85. 85. 85. 85. 85. 85. 85. 85.]
     [90. 90. 90. 90. 90. 90. 90. 90. 90.]]

    Get the coordinates of the centers of rolling windows with 50% overlap and
    an indexer that allows us to select points from each window:

    >>> window_size = 10  # degrees
    >>> window_coords, indices = rolling_window_spherical(
    ...     coordinates, window_size=window_size, overlap=0.5,
    ... )

    Window coordinates will be 1D arrays since the windows aren't regular.
    Their longitudinal size is calculated to preserve their area. Their shape
    is the number of windows generated:

    >>> print(window_coords[0].shape, window_coords[1].shape)
    (8,) (8,)

    The values of these arrays are the coordinates for the center of each
    rolling window. The latitude coordinates will be all at regular intervals
    dictated by the window size and the overlap:

    >>> print(window_coords[1])
    [65. 65. 70. 70. 75. 75. 80. 85.]

    But in longitude, the window sizes (and thus their centers) will spread out
    as latitude increases to balance the convergence of meridians. The window
    size in longitude will be:

    >>> window_size_lon = window_size / np.cos(np.radians(window_coords[1]))
    >>> print(np.array_str(window_size_lon, precision=1))
    [ 23.7  23.7  29.2  29.2  38.6  38.6  57.6 114.7]

    Notice that as we get closer to the pole the window size is larger than the
    region, so in these cases the windows cannot be guaranteed to have equal
    area. The center of each window will be:

    >>> print(np.array_str(window_coords[0], precision=1))
    [11.8 28.2 14.6 25.4 19.3 20.7 20.  20. ]

    If you look closely, you'll see that the amount of overlap between the
    windows isn't exactly 50%. This is because the overlap and window size do
    not result in multiples of the region. So we have to adjust the overlap to
    make things fit. This effect is less evident for smaller windows.

    The indices of points falling on each window will have the same shape as
    the window center coordinates:

    >>> print(indices.shape)
    (8,)

    Each element of the indices array is a tuple of arrays, one for each
    element in the ``coordinates``:

    >>> print(len(indices[0]))
    2

    They are indices of the points that fall inside the selected window (window
    0). The first element indexes the axis 0 of the coordinate arrays and so
    forth. So this:

    >>> print(indices[0][0])
    [0 0 0 0 0 1 1 1 1 1 2 2 2 2 2]

    corresponds to the rows of the coordinate arrays that belong to the first
    window, and this

    >>> print(indices[0][1])
    [0 1 2 3 4 0 1 2 3 4 0 1 2 3 4]

    corresponds to the columns of the coordinate arrays that belong to the
    first window.

    The same can be showed for the second window:

    >>> print(indices[1][0])
    [0 0 0 0 0 1 1 1 1 1 2 2 2 2 2]
    >>> print(indices[1][1])
    [4 5 6 7 8 4 5 6 7 8 4 5 6 7 8]

    and the third window:

    >>> print(indices[-1][0])
    [4 4 4 4 4 4 4 4 4 5 5 5 5 5 5 5 5 5 6 6 6 6 6 6 6 6 6]
    >>> print(indices[-1][1])
    [0 1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 8]

    Use these indices to select the coordinates the points that fall inside
    a window:

    >>> points_window_0 = [c[indices[0]] for c in coordinates]
    >>> print(points_window_0[0])
    [ 0.  5. 10. 15. 20.  0.  5. 10. 15. 20.  0.  5. 10. 15. 20.]
    >>> print(points_window_0[1])
    [60. 60. 60. 60. 60. 65. 65. 65. 65. 65. 70. 70. 70. 70. 70.]

    >>> points_window_1 = [c[indices[1]] for c in coordinates]
    >>> print(points_window_1[0])
    [20. 25. 30. 35. 40. 20. 25. 30. 35. 40. 20. 25. 30. 35. 40.]
    >>> print(points_window_1[1])
    [60. 60. 60. 60. 60. 65. 65. 65. 65. 65. 70. 70. 70. 70. 70.]

    If the coordinates are 1D, the indices will also be 1D:

    >>> coordinates1d = [c.ravel() for c in coordinates]
    >>> window_coords, indices = rolling_window_spherical(
    ...     coordinates1d, window_size=window_size, overlap=0.5,
    ... )
    >>> print(len(indices[0]))
    1

    In this case, the indices will refer to the raveled coordinate array. The
    indexer for the first window will be:

    >>> print(indices[0][0])
    [ 0  1  2  3  4  9 10 11 12 13 18 19 20 21 22]

    And for the second window:

    >>> print(indices[1][0])
    [ 4  5  6  7  8 13 14 15 16 17 22 23 24 25 26]

    The returned indices can be used in the same way as before to get the same
    coordinates:

    >>> print(coordinates1d[0][indices[0]])
    [ 0.  5. 10. 15. 20.  0.  5. 10. 15. 20.  0.  5. 10. 15. 20.]
    >>> print(coordinates1d[1][indices[0]])
    [60. 60. 60. 60. 60. 65. 65. 65. 65. 65. 70. 70. 70. 70. 70.]

    By default, the windows will span the entire data region. You can also
    control the specific region you'd like the windows to cover:

    >>> window_coords, indices = rolling_window_spherical(
    ...     coordinates,
    ...     window_size=window_size,
    ...     overlap=0.5,
    ...     region=(0, 20, 60, 75),
    ... )

    The windows will now try to fit the smaller region instead of the full
    extent of the coordinates:

    >>> print(coordinates[0][indices[0]])
    [ 0.  5. 10. 15. 20.  0.  5. 10. 15. 20.  0.  5. 10. 15. 20.]
    >>> print(coordinates[1][indices[0]])
    [60. 60. 60. 60. 60. 65. 65. 65. 65. 65. 70. 70. 70. 70. 70.]

    >>> print(coordinates[0][indices[1]])
    [ 0.  5. 10. 15. 20.  0.  5. 10. 15. 20.  0.  5. 10. 15. 20.]
    >>> print(coordinates[1][indices[1]])
    [65. 65. 65. 65. 65. 70. 70. 70. 70. 70. 75. 75. 75. 75. 75.]

    If the longitude range is a full 360 degrees, the windows will wrap around
    the 360-0 discontinuity:

    >>> coordinates = bd.grid_coordinates((0, 360, 0, 0), spacing=30)
    >>> print(coordinates[0])
    [[  0.  30.  60.  90. 120. 150. 180. 210. 240. 270. 300. 330. 360.]]
    >>> print(coordinates[1])
    [[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]

    >>> window_coords, indices = rolling_window_spherical(
    ...     coordinates, window_size=90, overlap=0.5,
    ... )
    >>> print(indices.shape)
    (8,)
    >>> print(coordinates[0][indices[0]])
    [  0.  30.  60.  90. 360.]

    The 360 point is there because it's the same as the 0 point and so they are
    both inside the window.

    The last window will be centered at 0 and will wrap around the 360-0
    divide:

    >>> print(coordinates[0][indices[-1]])
    [  0.  30. 330. 360.]

    This way, the windows wrap around the globe and overlap all the way around.
    """
    coordinates = check_coordinates(coordinates)
    check_coordinates_geographic(coordinates)
    check_overlap(overlap)
    if region is None:
        region = get_region(coordinates)
    check_region_geographic(region)
    region, coordinates = longitude_continuity(region, coordinates=coordinates)
    if window_size <= 0:
        message = f"Invalid window size '{window_size}'. Must be > 0."
        raise ValueError(message)
    # Check if longitude goes all the way around
    longitude_360 = np.allclose(abs(region[1] - region[0]), 360)
    # Calculate the window step based on the amount of overlap
    window_step = (1 - overlap) * window_size
    # We'll have to do this by bands of latitude. Each band will have
    # a different window size in longitude. See comments below for more
    # details.
    if window_size >= (region[3] - region[2]):
        # If the window size is larger than the region, line_coordinates
        # will through an error.
        bands = np.array([(region[3] + region[2]) / 2])
    else:
        # Always adjust the spacing to avoid falling out of valid geographic
        # boundaries.
        bands = line_coordinates(
            region[2] + window_size / 2,
            region[3] - window_size / 2,
            spacing=window_step,
            adjust="spacing",
        )
    # These will gather the window centers and indices of points inside each
    # window for each band. Window centers will later be concatenated into
    # a single array.
    longitude, latitude, indices1d = [], [], []
    # Need these so we can map the in-band data indices to the overall data
    # indices.
    data_indices = np.arange(coordinates[0].size)
    for central_latitude in bands:
        # Figure out the size in longitude that leads to equal area. See Malkin
        # (2016).
        window_size_lon = window_size / np.cos(np.radians(central_latitude))
        # Calculate the step size for longitude
        window_step_lon = (1 - overlap) * window_size_lon
        # Generate the longitudes of window centers in this band.
        if window_size_lon >= (region[1] - region[0]):
            # If the window size is larger than the region, line_coordinates
            # will through an error.
            band_longitude = np.array([(region[1] + region[0]) / 2])
        else:
            # Always adjust the spacing to make sure windows are evenly
            # distributed across the 360-0 boundary and the region doesn't
            # exceed valid intervals.
            band_longitude = line_coordinates(
                region[0] + window_size_lon / 2,
                region[1] - window_size_lon / 2,
                spacing=window_step_lon,
                adjust="spacing",
            )
        band_latitude = np.full_like(band_longitude, central_latitude)
        # Make a KD tree with points only in this band. This is needed because
        # query_ball_point only works for "square" windows and we'd select too
        # many points if using window_size_lon (with points out of the latitude
        # band) or too little if using window_size (since longitude intervals
        # are larger).
        latitude_min = central_latitude - window_size / 2
        latitude_max = central_latitude + window_size / 2
        in_band = np.logical_and(
            coordinates[1].ravel() >= latitude_min,
            coordinates[1].ravel() <= latitude_max,
        )
        band_coordinates = [c.ravel()[in_band] for c in coordinates]
        tree = KDTree(np.transpose(band_coordinates))
        # Use p=inf (infinity norm) to get square windows instead of circular.
        in_band_indices = tree.query_ball_point(
            np.transpose([band_longitude, band_latitude]),
            r=window_size_lon / 2,
            p=np.inf,
        )
        # Translate the in-band indices to the overall data indices
        band_indices1d = [data_indices[in_band][i] for i in in_band_indices]
        # If the longitude goes around the globe, add an extra window to have
        # continuity around the 360-0 boundary.
        if longitude_360:
            true_window_step_lon = band_longitude[1] - band_longitude[0]
            first_window_longitude = band_longitude[0] - true_window_step_lon
            first_window = (
                first_window_longitude - window_size_lon / 2,
                first_window_longitude + window_size_lon / 2,
                latitude_min,
                latitude_max,
            )
            first_window, band_coordinates = longitude_continuity(
                first_window,
                coordinates=band_coordinates,
            )
            tree = KDTree(np.transpose(band_coordinates))
            in_band_indices = tree.query_ball_point(
                np.array([[first_window_longitude, central_latitude]]),
                r=window_size_lon / 2,
                p=np.inf,
            )
            band_indices1d.extend(data_indices[in_band][i] for i in in_band_indices)
            band_longitude = np.append(band_longitude, first_window_longitude)
            band_latitude = np.append(band_latitude, central_latitude)
        latitude.append(band_latitude)
        longitude.append(band_longitude)
        indices1d.extend(band_indices1d)
    # Join results from all bands
    latitude = np.concatenate(latitude)
    longitude = np.concatenate(longitude)
    centers = (longitude, latitude)
    # Make an indices array for compatibility with the regular rolling window
    # function. But here the window coordinates cannot be a 2D array since
    # longitudinal windows are not regular.
    indices = np.fromiter(
        [
            np.unravel_index(np.array(i, dtype="int"), shape=coordinates[0].shape)
            for i in indices1d
        ],
        dtype="object",
    )
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
