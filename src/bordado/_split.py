"""
Functions to split points into blocks and windows.
"""
import numpy as np
from scipy.spatial import KDTree


def block_split(coordinates, *, block_shape=None, block_size=None, adjust="spacing", region=None):
    """
    Split a region into blocks and label points according to where they fall.

    The labels are integers corresponding to the index of the block. Also
    returns the coordinates of the center of each block (following the same
    index as the labels).

    Blocks can be specified by their size or the number of blocks in each
    dimension (the shape).

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. The arrays can be
        n-dimensional.
    shape : tuple = (..., n_north, n_east) or None
        The number of blocks in the South-North and West-East directions,
        respectively.
    spacing : float, tuple = (..., space_north, space_east), or None
        The block size in the South-North and West-East directions,
        respectively. A single value means that the size is equal in both
        directions.
    adjust : {'spacing', 'region'}
        Whether to adjust the spacing or the region if required. Ignored if
        *shape* is given instead of *spacing*. Defaults to adjusting the
        spacing.
    region : list = [W, E, S, N]
        The boundaries of a given region in Cartesian or geographic
        coordinates. If not region is given, will use the bounding region of
        the given points.

    Returns
    -------
    block_coordinates : tuple of arrays
        (easting, northing) arrays with the coordinates of the center of each
        block.
    labels : array
        integer label for each data point. The label is the index of the block
        to which that point belongs.

    Examples
    --------
    >>> from verde import grid_coordinates
    >>> coords = grid_coordinates((-5, 0, 5, 10), spacing=1)
    >>> block_coords, labels = block_split(coords, spacing=2.5)
    >>> for coord in block_coords:
    ...     print(', '.join(['{:.2f}'.format(i) for i in coord]))
    -3.75, -1.25, -3.75, -1.25
    6.25, 6.25, 8.75, 8.75
    >>> print(labels.reshape(coords[0].shape))
    [[0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [2 2 2 3 3 3]
     [2 2 2 3 3 3]
     [2 2 2 3 3 3]]
    >>> # Use the shape instead of the block size
    >>> block_coords, labels = block_split(coords, shape=(4, 2))
    >>> for coord in block_coords:
    ...     print(', '.join(['{:.3f}'.format(i) for i in coord]))
    -3.750, -1.250, -3.750, -1.250, -3.750, -1.250, -3.750, -1.250
    5.625, 5.625, 6.875, 6.875, 8.125, 8.125, 9.375, 9.375
    >>> print(labels.reshape(coords[0].shape))
    [[0 0 0 1 1 1]
     [0 0 0 1 1 1]
     [2 2 2 3 3 3]
     [4 4 4 5 5 5]
     [6 6 6 7 7 7]
     [6 6 6 7 7 7]]

    """
    # Select the coordinates after checking to make sure indexing will still
    # work on the ignored coordinates.
    coordinates = check_coordinates(coordinates)[:2]
    if region is None:
        region = get_region(coordinates)
    block_coords = grid_coordinates(
        region, spacing=spacing, shape=shape, adjust=adjust, pixel_register=True
    )

    points = np.transpose(n_1d_arrays(coordinates, len(coordinates)))
    tree = cKDTree(points, **kwargs)

    tree = kdtree(block_coords)

    labels = tree.query(np.transpose(n_1d_arrays(coordinates, 2)))[1]
    return n_1d_arrays(block_coords, len(block_coords)), labels
