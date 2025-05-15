# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions to calculate the distances between neighbors.
"""

import numpy as np
import scipy.spatial

from ._validation import check_coordinates


def neighbor_distance_statistics(coordinates, statistic, *, k=1):
    """
    Calculate statistics of the distances to the k-nearest neighbors of points.

    For each point specified in *coordinates*, calculate the given statistic on
    the Cartesian distance to its *k* neighbors among the other points in the
    dataset.

    Useful for finding mean/median distances between points, general point
    spread (standard deviation), variability of neighboring distances
    (peak-to-peak), etc.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Should be in an
        order compatible with the order of boundaries in *region*. Arrays can
        be Python lists. Arrays can be of any shape but must all have the same
        shape.
    statistic : str
        Which statistic to calculate for the distances of the k-nearest
        neighbors of each point. Valid values are: ``"mean"``,  ``"median"``,
        ``"std"`` (standard deviation),  ``"var"`` (variance),  ``"ptp"``
        (peak-to-peak amplitude).
    k : int
        Will calculate the median of the *k* nearest neighbors of each point. A
        value of 1 will result in the distance to nearest neighbor of each data
        point. Must be >= 1. Default is 1.

    Returns
    -------
    statistics : array
        An array with the statistic of the k-nearest neighbor distances of each
        point. The array will have the same shape as the input coordinate
        arrays.

    Raises
    ------
    ValueError
        If *k* is less than 1, if the *statistic* is invalid, or if coordinate
        arrays have different shapes.

    Notes
    -----
    To get the average point spacing for sparse uniformly spaced datasets,
    calculating the mean/median using *k* of 1 is reasonable. Datasets with
    points clustered into tight groups (e.g., densely sampled along a flight
    line or ship track) will have very small distances to the closest
    neighbors, which is not representative of the actual median spacing of
    points because it doesn't take the spacing between lines into account. In
    these cases, a median of the 10-20 or more nearest neighbors might be more
    representative.

    Examples
    --------
    Generate a grid of points for an example:

    >>> import bordado as bd
    >>> coordinates = bd.grid_coordinates((5, 10, -20, -17), spacing=1)
    >>> print(coordinates[0])
    [[ 5.  6.  7.  8.  9. 10.]
     [ 5.  6.  7.  8.  9. 10.]
     [ 5.  6.  7.  8.  9. 10.]
     [ 5.  6.  7.  8.  9. 10.]]
    >>> print(coordinates[1])
    [[-20. -20. -20. -20. -20. -20.]
     [-19. -19. -19. -19. -19. -19.]
     [-18. -18. -18. -18. -18. -18.]
     [-17. -17. -17. -17. -17. -17.]]

    The mean of the distance to 1 nearest neighbor should be the grid spacing:

    >>> mean_distances = neighbor_distance_statistics(coordinates, "mean", k=1)
    >>> print(mean_distances)
    [[1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]]

    The statistics returned have the same shape as the input coordinates:

    >>> print(mean_distances.shape, coordinates[0].shape)
    (4, 6) (4, 6)
    >>> mean_distances = neighbor_distance_statistics(
    ...     [c.ravel() for c in coordinates], "mean", k=1,
    ... )
    >>> print(mean_distances.shape)
    (24,)

    The mean distance to the 2 nearest points should also all be 1 since they
    are the neighbors along the rows and columns of the matrix:

    >>> mean_distances = neighbor_distance_statistics(coordinates, "mean", k=2)
    >>> print(mean_distances)
    [[1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]]

    The distance to the 3 nearest points is 1 but on the corners of the grid,
    the distances are [1, 1, sqrt(2)] which leads to a median of 1:

    >>> median_distances = neighbor_distance_statistics(
    ...     coordinates, "median", k=3,
    ... )
    >>> print(median_distances)
    [[1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1. 1.]]

    But using the 4 nearest points leads to distances [1, 1, sqrt(2), 2] at the
    corners, which results in a median of 1.21.

    >>> median_distances = neighbor_distance_statistics(
    ...     coordinates, "median", k=4,
    ... )
    >>> for line in median_distances:
    ...     print(" ".join([f"{i:.2f}" for i in line]))
    1.21 1.00 1.00 1.00 1.00 1.21
    1.00 1.00 1.00 1.00 1.00 1.00
    1.00 1.00 1.00 1.00 1.00 1.00
    1.21 1.00 1.00 1.00 1.00 1.21

    """
    coordinates = check_coordinates(coordinates)
    if k < 1:
        message = f"Invalid number of neighbors 'k={k}'. Must be >= 1."
        raise ValueError(message)
    statistics = {
        "mean": np.mean,
        "median": np.median,
        "std": np.std,
        "var": np.var,
        "ptp": np.ptp,
    }
    if statistic not in statistics:
        message = (
            f"Invalid statistic '{statistic}'. Must be one of: {statistics.keys()}."
        )
        raise ValueError(message)
    shape = np.broadcast(*coordinates).shape
    transposed_coordinates = np.transpose([c.ravel() for c in coordinates])
    tree = scipy.spatial.KDTree(transposed_coordinates)
    # The k=1 nearest point is going to be the point itself (with a distance of
    # zero) because we don't remove each point from the dataset in turn. We
    # don't care about that distance so start with the second closest. Only get
    # the first element returned (the distance) and ignore the rest (the
    # neighbor indices).
    k_distances = tree.query(transposed_coordinates, k=k + 1)[0][:, 1:]
    result = statistics[statistic](k_distances, axis=1)
    return result.reshape(shape)
