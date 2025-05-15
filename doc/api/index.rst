.. _api:

List of functions and classes (API)
===================================

.. automodule:: bordado

.. currentmodule:: bordado

Coordinate generation
---------------------

.. autosummary::
   :toctree: generated/

   line_coordinates
   random_coordinates
   grid_coordinates
   profile_coordinates

Regions and bounding boxes
--------------------------

.. autosummary::
   :toctree: generated/

   inside
   get_region
   pad_region

Splitting points into blocks and windows
----------------------------------------

.. autosummary::
   :toctree: generated/

   block_split
   expanding_window
   rolling_window

Other utilities
---------------

.. autosummary::
   :toctree: generated/

   neighbor_distance_statistics
   spacing_to_size
   shape_to_spacing

Validation of inputs
--------------------

.. autosummary::
   :toctree: generated/

   check_coordinates
   check_region
   check_shape
