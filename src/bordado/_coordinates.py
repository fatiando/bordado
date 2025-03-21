# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Functions for validating and manipulation coordinate arrays.
"""

import numpy as np


def check_coordinates(coordinates):
    """
    Check that coordinate arrays all have the same shape.

    Parameters
    ----------
    coordinates : tuple = (easting, northing, ...)
        Tuple of arrays with the coordinates of each point. Arrays can be
        Python lists.

    Returns
    -------
    coordinates : tuple = (easting, northing, ...)
        Tuple of coordinate arrays, converted to numpy arrays if necessary.

    Raises
    ------
    ValueError
        If the coordinates don't have the same shape.
    """
    coordinates = tuple(np.asarray(c) for c in coordinates)
    shapes = [c.shape for c in coordinates]
    if not all(shape == shapes[0] for shape in shapes):
        message = (
            "Invalid coordinates. All coordinate arrays must have the same shape. "
            f"Given coordinate shapes: {shapes}"
        )
        raise ValueError(message)
    return coordinates
