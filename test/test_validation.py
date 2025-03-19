# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the input and output validation functions.
"""

import pytest

from bordado._validation import check_region


@pytest.mark.parametrize(
    ("region", "message"),
    [
        ([], "Invalid region .* Only 4 values"),
        ([1, 2, 3, 4, 5], "Invalid region .* Only 4 values"),
        ([1, 2, 3], "Invalid region .* Only 4 values"),
        ([1, 2, 3, 1], "Invalid region .* S <= N"),
        ([2, 1, 3, 4], "Invalid region .* W <= E"),
        ([-1, -2, -4, -3], "Invalid region .* W <= E"),
        ([-2, -1, -2, -3], "Invalid region .* S <= N"),
    ],
)
def test_check_region_raises(region, message):
    """Make sure an exception is raised for bad regions."""
    with pytest.raises(ValueError, match=message):
        check_region(region)


@pytest.mark.parametrize(
    "region",
    [
        [1, 2, 3, 4],
        [-2, -1, -5, -4],
    ],
)
def test_check_region_passes(region):
    """Check that valid regions don't cause exceptions."""
    check_region(region)
