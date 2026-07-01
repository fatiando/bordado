# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Extra utility functions that don't fall into other categories.
"""

import numpy as np


def make_non_dimensional_coordinates(values, shape, dtype):
    """
    Make a list of arrays with the given values of non-dimensional coordinates.

    These are coordinates that are not part of the dimensions of a grid or
    spread of points. Think of them as extra coordinates.

    Parameters
    ----------
    values : None or float or list or array
        The values of the non-dimensional coordinates. If None, an empty list
        will be returned. If a float, will generate one array of the desired
        shape with this value as the fill. If a list or array, will generate
        one array of the given shape per value in the list or array.
    shape : tuple
        The shape of the desired array(s).
    dtype : str
        A numpy compatible dtype used for the output array.

    Returns
    -------
    coordinates : list
        List of arrays generated. Even if a single value is passed, the output
        will still be a list with a single array.

    Examples
    --------
    Generating a single array:

    >>> make_non_dimensional_coordinates(10, (2,), dtype="int")
    [array([10, 10])]
    >>> make_non_dimensional_coordinates(10, (2, 2), dtype="int")
    [array([[10, 10],
           [10, 10]])]

    To generate multiple arrays:

    >>> make_non_dimensional_coordinates([10, 20], (2,), dtype="int")
    [array([10, 10]), array([20, 20])]
    >>> import numpy as np
    >>> make_non_dimensional_coordinates(np.array([10, 20]), (2,), dtype="int")
    [array([10, 10]), array([20, 20])]
    >>> make_non_dimensional_coordinates(
    ...     np.array([[10], [20]]), (2,), dtype="int",
    ... )
    [array([10, 10]), array([20, 20])]

    If None is given:

    >>> make_non_dimensional_coordinates(None, (2,), dtype="int")
    []
    """
    coordinates = []
    if values is not None:
        for value in np.atleast_1d(values).ravel():
            coordinates.append(np.full(shape, value, dtype=dtype))
    return coordinates
