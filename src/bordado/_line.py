# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Generate regular coordinates along lines and grids.
"""

import numpy as np


def line_coordinates(
    start, stop, *, size=None, spacing=None, adjust="spacing", pixel_register=False
):
    """
    Generate evenly spaced points between two values.

    Able to handle either specifying the number of points required (*size*) or
    the size of the interval between points (*spacing*). If using *size*, the
    output will be similar to using :func:`numpy.linspace`. When using
    *spacing*, if the interval is not divisible by the desired spacing, either
    the interval or the spacing will have to be adjusted. By default, the
    spacing will be rounded to the nearest multiple. Optionally, the *start*
    and *stop* values (the region) can be adjusted to fit the exact spacing
    given.

    Parameters
    ----------
    start : float
        The starting value of the sequence.
    stop : float
        The end value of the sequence.
    size : int or None
        The number of points in the sequence. If None, *spacing* must be
        provided.
    spacing : float or None
        The step size (interval) between points in the sequence. If None,
        *size* must be provided.
    adjust : {'spacing', 'region'}
        Whether to adjust the spacing or the interval/region if required.
        Ignored if *size* is given instead of *spacing*. Defaults to adjusting
        the spacing.
    pixel_register : bool
        If True, the points will refer to the center of each interval (pixel)
        instead of the boundaries. In practice, this means that there will be
        one less element in the sequence if *spacing* is provided. If *size* is
        provided, the requested number of elements is respected. Default is
        False.

    Returns
    -------
    sequence : array
        The generated sequence of values.

    Examples
    --------
    >>> values = line_coordinates(0, 5, spacing=2.5)
    >>> print(values.shape)
    (3,)
    >>> print(values)
    [0.  2.5 5. ]
    >>> print(line_coordinates(0, 10, size=5))
    [ 0.   2.5  5.   7.5 10. ]
    >>> print(line_coordinates(0, 10, spacing=2.5))
    [ 0.   2.5  5.   7.5 10. ]

    The spacing is adjusted to fit the interval by default but this can be
    changed to adjusting the interval/region instead:

    >>> print(line_coordinates(0, 10, spacing=2.4))
    [ 0.   2.5  5.   7.5 10. ]
    >>> print(line_coordinates(0, 10, spacing=2.4, adjust="region"))
    [0.2 2.6 5.  7.4 9.8]
    >>> print(line_coordinates(0, 10, spacing=2.6))
    [ 0.   2.5  5.   7.5 10. ]
    >>> print(line_coordinates(0, 10, spacing=2.6, adjust="region"))
    [-0.2  2.4  5.   7.6 10.2]

    Optionally, return values at the center of the intervals instead of their
    boundaries:

    >>> print(line_coordinates(0, 10, spacing=2.5, pixel_register=True))
    [1.25 3.75 6.25 8.75]

    Notice that this produces one value less than the non-pixel registered
    version. If using *size* instead of *spacing*, the number of values will be
    *size* regardless and the spacing will therefore be different from the
    non-pixel registered version:

    >>> print(line_coordinates(0, 10, size=5, pixel_register=True))
    [1. 3. 5. 7. 9.]

    """
    if size is not None and spacing is not None:
        message = "Both size and spacing provided. Only one is allowed."
        raise ValueError(message)
    if size is None and spacing is None:
        message = "Either a size or a spacing must be provided."
        raise ValueError(message)
    if spacing is not None:
        size, start, stop = _spacing_to_size(start, stop, spacing, adjust)
    elif pixel_register and size is not None:
        # Starts by generating grid-line registered coordinates and shifting
        # them to the center of the pixel. Need 1 more point if given a size
        # instead of spacing so that we can do that because we discard the last
        # point when shifting the coordinates.
        size = size + 1
    values = np.linspace(start, stop, size)
    if pixel_register:
        values = values[:-1] + (values[1] - values[0]) / 2
    return values


def _spacing_to_size(start, stop, spacing, adjust):
    """
    Convert a spacing to the number of points between start and stop.

    Takes into account if the spacing or the interval needs to be adjusted.

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

    """
    if adjust not in ["spacing", "region"]:
        message = (
            f"Invalid value for 'adjust' argument '{adjust}'. "
            "Should be 'spacing' or 'region'"
        )
        raise ValueError(message)
    # Add 1 to get the number of nodes, not segments
    size = int(round((stop - start) / spacing) + 1)
    # If the spacing >= 2 * (stop - start), it rounds to zero so we'd be
    # generating a single point, which isn't equivalent to adjusting the
    # spacing or the region. To get the appropriate behaviour of decreasing the
    # spacing until it fits the region or increasing the region until it fits
    # at least 1 spacing, we need to always round to at least 1 in the code
    # above.
    if size == 1:
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
