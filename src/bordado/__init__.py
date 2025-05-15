# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
These are the functions and classes that make up the Bordado API.
"""

from ._distance import neighbor_distance_statistics
from ._grid import grid_coordinates
from ._line import line_coordinates
from ._profile import great_circle_coordinates, profile_coordinates
from ._random import random_coordinates
from ._region import get_region, inside, pad_region
from ._split import block_split, expanding_window, rolling_window
from ._utils import shape_to_spacing, spacing_to_size
from ._version import __version__

# Append a leading "v" to the generated version by setuptools_scm
__version__ = f"v{__version__}"
