.. _tutorial_profile:

Profiles between two points
===========================

It's common to need evenly spaced coordinate values between two points
to extract or interpolate profiles from regular grid data. Bordado
offers functions :func:`bordado.profile_coordinates` (Cartesian) and
:func:`bordado.great_circle_coordinates` (spherical) to generate these
coordinates. Let's see how we can use them!

.. jupyter-execute::

    import bordado as bd
    import matplotlib.pyplot as plt
    import pygmt

Coordinates between two points in 2D
------------------------------------


Coordinates in more dimensions
------------------------------


Coordinates along a great circle path
-------------------------------------
