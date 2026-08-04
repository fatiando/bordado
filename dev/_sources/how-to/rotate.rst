.. _how_to_rotate:

Rotate coordinates in 2D
------------------------

Let's say we have some 2D coordinates from a dataset, like easting and northing
in some projection, and we wish to rotate them. This could be useful, for
example, if we're using those coordinates to build a synthetic dataset. Or
maybe we need to align the coordinates with a certain axis in order to do some
processing. Whatever the use case, :func:`bordado.rotate_coordinates` will do
the operation for us.

.. jupyter-execute::

    import ensaio
    import pyproj
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import bordado as bd

To demonstrate, we'll first load some bathymetry data from the Caribbean using
:func:`ensaio.fetch_caribbean_bathymetry`:

.. jupyter-execute::

    fname = ensaio.fetch_caribbean_bathymetry(version=2)
    data = pd.read_csv(fname)
    data

The data are all in geographic longitude and latitude coordinates. We'll
first project them to Cartesian coordinates using :mod:`pyproj` since rotating
curvilinear geographic coordinates doesn't make much sense:

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    coordinates = projection(data.longitude, data.latitude)

Now we can plot the data using matplotlib:

.. jupyter-execute::

    plt.figure(figsize=(8, 5), layout="constrained")
    plt.scatter(*coordinates, c=data.bathymetry_m, s=0.5)
    plt.colorbar(label="meters")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.axis("scaled")
    plt.show()

We can rotate the coordinates **counterclockwise** by providing a
positive angle to :func:`~bordado.rotate_coordinates`:

.. jupyter-execute::

    rotated = bd.rotate_coordinates(coordinates, angle=45)

    plt.figure(layout="constrained")
    plt.scatter(*rotated, c=data.bathymetry_m, s=0.5)
    plt.colorbar(label="meters")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.title("Counterclockwise rotation")
    plt.axis("scaled")
    plt.show()

Or **clockwise** by providing a negative angle:

.. jupyter-execute::

    rotated = bd.rotate_coordinates(coordinates, angle=-45)

    plt.figure(layout="constrained")
    plt.scatter(*rotated, c=data.bathymetry_m, s=0.5)
    plt.colorbar(label="meters")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.title("Clockwise rotation")
    plt.axis("scaled")
    plt.show()

**Notice that the range of the coordinates changes quite a bit.** This is
because the rotation is done around the origin of the coordinate system at point
(0, 0).

To rotate around the center of the dataset and retain approximately the original
range of the coordinates, we can specify the ``rotation_center`` argument:

.. jupyter-execute::

    rotated = bd.rotate_coordinates(
        coordinates,
        angle=-45,
        rotation_center=[np.median(c) for c in coordinates],
    )

    plt.figure(layout="constrained")
    plt.scatter(*rotated, c=data.bathymetry_m, s=0.5)
    plt.colorbar(label="meters")
    plt.xlabel("Easting (m)")
    plt.ylabel("Northing (m)")
    plt.title("Clockwise rotation")
    plt.axis("scaled")
    plt.show()

In this case, the layout of the points looks exactly the same as previously,
but the range of the coordinates matches the original dataset more closely.
