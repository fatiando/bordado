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


def neighbor_distance_statistics(coordinates, *, k_nearest=1, statistic="mean"):
    """
    Median distance between the *k* nearest neighbors of each point.

    For each point specified in *coordinates*, calculate the median of the
    Cartesian distance to its *k_nearest* neighbors among the other points in
    the dataset.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Should be in an
        order compatible with the order of boundaries in *region*. Arrays can
        be Python lists. Arrays can be of any shape but must all have the same
        shape.
    k_nearest : int
        Will calculate the median of the *k* nearest neighbors of each point. A
        value of 1 will result in the distance to nearest neighbor of each data
        point. Must be >= 1. Default is 1.

    Returns
    -------
    distances : array
        An array with the median distances to the *k* nearest neighbors of each
        data point. The array will have the same shape as the input coordinate
        arrays.

    Notes
    -----
    To get the average point spacing for sparse uniformly spaced datasets,
    using *k_nearest* of 1 is reasonable. Datasets with points clustered into
    tight groups (e.g., densely sampled along a flight line or ship track) will
    have very small distances to the closest neighbors, which is not
    representative of the actual median spacing of points because it doesn't
    take the spacing between lines into account. In these cases, a median of
    the 10-20 or more nearest neighbors might be more representative.

    Examples
    --------
    >>> import bordado as bd
    >>> import numpy as np
    >>> coords = bd.grid_coordinates((5, 10, -20, -17), spacing=1)
    >>> # The nearest neighbor distance should be the grid spacing
    >>> distance = median_distance(coords, k_nearest=1)
    >>> np.allclose(distance, 1)
    True
    >>> # The distance has the same shape as the coordinate arrays
    >>> print(distance.shape, coords[0].shape)
    (4, 6) (4, 6)
    >>> # The 2 nearest points should also all be at a distance of 1
    >>> distance = median_distance(coords, k_nearest=2)
    >>> np.allclose(distance, 1)
    True
    >>> # The 3 nearest points are at a distance of 1 but on the corners they
    >>> # are [1, 1, sqrt(2)] away. The median for these points is also 1.
    >>> distance = median_distance(coords, k_nearest=3)
    >>> np.allclose(distance, 1)
    True
    >>> # The 4 nearest points are at a distance of 1 but on the corners they
    >>> # are [1, 1, sqrt(2), 2] away.
    >>> distance = median_distance(coords, k_nearest=4)
    >>> print("{:.2f}".format(np.median([1, 1, np.sqrt(2), 2])))
    1.21
    >>> for line in distance:
    ...     print(" ".join(["{:.2f}".format(i) for i in line]))
    1.21 1.00 1.00 1.00 1.00 1.21
    1.00 1.00 1.00 1.00 1.00 1.00
    1.00 1.00 1.00 1.00 1.00 1.00
    1.21 1.00 1.00 1.00 1.00 1.21

    """
    coordinates = check_coordinates(coordinates)
    if k_nearest < 1:
        message = f"Invalid number of neighbors 'k_nearest={k_nearest}'. Must be >= 1."
        raise ValueError(message)
    shape = np.broadcast(*coordinates).shape
    transposed_coordinates = np.transpose([c.ravel() for c in coordinates])
    tree = scipy.spatial.KDTree(transposed_coordinates)
    # The k=1 nearest point is going to be the point itself (with a distance of
    # zero) because we don't remove each point from the dataset in turn. We
    # don't care about that distance so start with the second closest. Only get
    # the first element returned (the distance) and ignore the rest (the
    # neighbor indices).
    k_distances = tree.query(transposed_coordinates, k=k_nearest + 1)[0][:, 1:]
    distances = np.median(k_distances, axis=1)
    return distances.reshape(shape)
