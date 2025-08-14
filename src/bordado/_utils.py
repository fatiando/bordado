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

from ._validation import check_adjust, check_region, check_shape


def spacing_to_size(start, stop, spacing, *, adjust="spacing"):
    """
    Convert a spacing to the number of points between start and stop.

    Takes into account if the spacing or the interval needs to be adjusted in
    order to fit exactly. This is needed when the interval is not a multiple of
    the spacing.

    Parameters
    ----------
    start : float
        The starting value of the sequence.
    stop : float
        The end value of the sequence.
    spacing : float
        The step size (interval) between points in the sequence.
    adjust : {'spacing', 'region'}
        Whether to adjust the spacing or the interval/region if required.
        Defaults to adjusting the spacing.

    Returns
    -------
    size : int
        The number of points between start and stop.
    start : float
        The end of the interval, which may or may not have been adjusted.
    stop : float
        The end of the interval, which may or may not have been adjusted.

    Examples
    --------
    If the spacing is a multiple of the interval, then the size is how many
    points fit in the interval and the start and stop values are maintained:

    >>> size, start, stop = spacing_to_size(0, 1, 0.5)
    >>> print(size, start, stop)
    3 0 1

    If the spacing is not a multiple, then it will be adjusted to fit the
    interval by default. In this case, then number of points remains the same:

    >>> size, start, stop = spacing_to_size(0, 1, 0.6)
    >>> print(size, start, stop)
    3 0 1

    Alternatively, we can ask it to adjust the region instead of the spacing
    between points:

    >>> size, start, stop = spacing_to_size(0, 1, 0.6, adjust="region")
    >>> print(f"{size} {start:.1f} {stop:.1f}")
    3 -0.1 1.1

    If the start and stop are the same, only a single point will be generated:

    >>> size, start, stop = spacing_to_size(1e-8, 1e-8, 1e-7)
    >>> print(f"{size} {start:.1g} {stop:.1g}")
    1 1e-08 1e-08
    """
    check_adjust(adjust)
    # Add 1 to get the number of nodes, not segments
    size = int(round((stop - start) / spacing) + 1)
    # If the spacing >= 2 * (stop - start), it rounds to zero so we'd be
    # generating a single point, which isn't equivalent to adjusting the
    # spacing or the region. To get the appropriate behaviour of decreasing the
    # spacing until it fits the region or increasing the region until it fits
    # at least 1 spacing, we need to always round to at least 1 in the code
    # above. But this should only be done if the interval stop - start is not
    # close to zero.
    if size == 1 and not np.isclose(stop, start):
        # if size == 1:
        size += 1
    if adjust == "region":
        # The size is the same but we adjust the interval so that the spacing
        # isn't altered when we do the linspace.
        required_length = (size - 1) * spacing
        given_length = stop - start
        pad = (required_length - given_length) / 2
        stop = stop + pad
        start = start - pad
    return size, start, stop


def shape_to_spacing(region, shape, *, pixel_register=False):
    """
    Calculate the spacing of a regular grid given a region and shape.

    The spacing is assumed to be constant along each direction but can vary
    between directions.

    Parameters
    ----------
    region : tuple = (W, E, S, N, ...)
        The boundaries of a given region in Cartesian or geographic
        coordinates. Should have a lower and an upper boundary for each
        dimension of the coordinate system.
    shape : tuple = (..., size_SN, size_WE)
        The number of points in each direction of the given region, in reverse
        order. Must have one integer value per dimension of the region. The
        order of arguments is the opposite of the order of the region for
        compatibility with numpy's ``.shape`` attribute.
    pixel_register : bool
        If True, the coordinates will refer to the center of each grid pixel
        instead of the grid lines. In practice, this means that there will be
        one less element per dimension of the grid when compared to grid line
        registered. Default is False.

    Returns
    -------
    spacing : tuple = (..., space_SN, space_WE)
        The grid spacing in each direction of the given region, in reverse
        order. Has one value per dimension of the region. The order of
        arguments is the opposite of the order of the region for compatibility
        with *shape*.

    Examples
    --------
    For 2-dimensional grids, the region has 4 elements and the shape must have
    2 elements:

    >>> spacing = shape_to_spacing((0, 10, -5, 1), (7, 11))
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}")
    1.0, 1.0

    The spacing doesn't have to be the same in each direction:

    >>> spacing = shape_to_spacing((0, 10, -5, 1), (14, 11))
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}")
    0.5, 1.0

    Notice that the spacing is in the same order as the shape:

    >>> spacing = shape_to_spacing((0, 10, -5, 1), (7, 21))
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}")
    1.0, 0.5

    Pixel registration is also supported:

    >>> spacing = shape_to_spacing(
    ...     (-0.5, 10.5, -5.5, 1.5), (7, 11), pixel_register=True,
    ... )
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}")
    1.0, 1.0
    >>> spacing = shape_to_spacing(
    ...     (-0.25, 10.25, -5.5, 1.5), (7, 21), pixel_register=True,
    ... )
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}")
    1.0, 0.5

    Grids don't have to be 2-dimensional:

    >>> spacing = shape_to_spacing((0, 10, -5, 1, 10, 14), (5, 7, 11))
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}, {spacing[2]:.1f}")
    1.0, 1.0, 1.0
    >>> spacing = shape_to_spacing(
    ...     (-0.25, 10.25, -5.5, 1.5, -0.1, 1.1), (5, 7, 21), pixel_register=True,
    ... )
    >>> print(f"{spacing[0]:.1f}, {spacing[1]:.1f}, {spacing[2]:.1f}")
    0.2, 1.0, 0.5
    """
    check_region(region)
    check_shape(shape, region)
    spacing = []
    for i, n in enumerate(reversed(shape)):
        n_points = n
        if not pixel_register:
            n_points -= 1
        spacing.append((region[2 * i + 1] - region[2 * i]) / n_points)
    return tuple(reversed(spacing))


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
