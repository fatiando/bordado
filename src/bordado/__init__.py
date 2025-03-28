# Copyright (c) 2025 The Bordado Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
These are the functions and classes that make up the Bordado API.
"""

from ._coordinates import check_coordinates
from ._grid import grid_coordinates
from ._line import line_coordinates
from ._random import random_coordinates
from ._region import check_region, get_region, inside, pad_region
from ._split import block_split, rolling_window
from ._version import __version__

# Append a leading "v" to the generated version by setuptools_scm
__version__ = f"v{__version__}"
