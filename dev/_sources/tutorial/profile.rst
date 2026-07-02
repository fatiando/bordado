.. _tutorial_profile:

Profiles between two points
===========================

It's common to need evenly spaced coordinate values between two points
to extract or interpolate profiles from regular grid data. However,
generating such points is not always trivial, particularly when we
want to take the curvature of the Earth into account or want to specify
the spacing between points instead of the number of points. Bordado
offers functions :func:`bordado.profile_coordinates` (Cartesian) and
:func:`bordado.great_circle_coordinates` (spherical) to generate these
coordinates. Let's see how we can use them!

.. jupyter-execute::

    import bordado as bd
    import numpy as np
    import matplotlib.pyplot as plt
    import pygmt

Coordinates between two points in 2D
------------------------------------

Let's say we have the 2D coordinates (think easting and northing, for example) for two
points:

.. jupyter-execute::

    beginning = (0, 0)  # easting, northing
    end = (10, 5)

    # Make a region for plotting later
    region = bd.pad_region(bd.get_region(np.transpose((beginning, end))), 2)
    print(region)

.. tip::

    Functions :func:`bordado.get_region` and :func:`bordado.pad_region`
    are very useful to extracting and modifying region information for plotting,
    interpolation, and more!

We can use :func:`bordado.profile_coordinates` to make coordinates for
evenly spaced points between them like so:

.. jupyter-execute::

    coordinates, distances = bd.profile_coordinates(
        beginning, end, spacing=0.5,
    )

The function returns the coordinates of the points as a tuple of two arrays:

.. jupyter-execute::

    for i, c in enumerate(coordinates):
        print(f"coordinate {i}:\n{c}\n")

Let's plot the two reference points and the profile points:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(8, 6), layout="constrained")
    ax.plot(*beginning, "^", markersize=12, label="Beginning")
    ax.plot(*end, "v", markersize=12, label="End")
    ax.plot(*coordinates, ".-", label="Profile")
    ax.legend()
    ax.grid()
    ax.set_xlim(*region[:2])
    ax.set_ylim(*region[2:])
    ax.set_xlabel("Easting")
    ax.set_ylabel("Northing")
    ax.set_aspect("equal")
    plt.show()

The second argument that is returned is an array with the distances between
points along the profile:

.. jupyter-execute::

    print(distances)

Notice that they are not exactly multiples of the spacing because the length of
the profile was a not a multiple of it, and so the spacing was adjusted.

.. note::

    There's no option to adjust the region here since that would mean moving the
    beginning and end points of the profile.


Coordinates in more dimensions
------------------------------

We can also generate these profile points in more than 2 dimensions. To do so,
we just have to specify the coordinates of the beginning and end points with
more than 2 dimensions:

.. jupyter-execute::

    beginning = (0, 0, 0)  # easting, northing, upward
    end = (10, 5, 7)

    coordinates, distances = bd.profile_coordinates(
        beginning, end, spacing=0.5,
    )

    for i, c in enumerate(coordinates):
        print(f"coordinate {i}:\n{c}\n")

    print(f"distances:\n{distances}")

Notice that now we have 3 coordinate arrays in the output, each starting and
finishing at the corresponding values of the beginning and end points. The
spacing was also adjusted to match the length of the 3D vector between the two
points.


Coordinates along a great circle path
-------------------------------------

If our coordinates are geographic longitude and latitude (angles
in degrees or radians), we probably don't want to use them with
:func:`bordado.profile_coordinates` since that would assume that they are
Cartesian coordinates. In these cases, we generally want the **shortest path
along the surface of a sphere**. This is called a **great circle** and we can
generate coordinates along one using :func:`bordado.great_circle_coordinates`.

Let's set up our two points on the sphere with coordinates in degrees and plot
them on a map with :mod:`pygmt`:

.. jupyter-execute::

    são_paulo = (-46.7011, -23.5604)  # longitude, latitude (degrees)
    luanda = (13.2559, -8.8549)

    fig = pygmt.Figure()
    fig.coast(land="#cccccc", region="g", projection="G-20/0/20c", frame="afg")
    fig.plot(x=são_paulo[0], y=são_paulo[1], style="i0.5c", fill="seagreen", label="São Paulo")
    fig.plot(x=luanda[0], y=luanda[1], style="t0.5c", fill="orange", label="Luanda")
    fig.legend(position="jTR+l2p")
    fig.show()

Now we can make a great circle path between them with points at every 100 km
(100,000 meters) like so:

.. jupyter-execute::

    coordinates, distances = bd.great_circle_coordinates(
        são_paulo, luanda, spacing=100_000,
    )

The coordinates are a tuple of two arrays with the longitude and latitude of the
points in degrees:

.. jupyter-execute::

    print(f"longitude:\n{coordinates[0]}\n")
    print(f"latitude:\n{coordinates[1]}\n")

Notice that both arrays start at the coordinates for São Paulo and end at the
coordinates for Luanda.

The distances are the great circle distances between points in the profile and the starting point (São Paulo) in meters:

.. jupyter-execute::

    print(distances)

Again, notice that these are approximately the chosen spacing but not exactly
since they had to be adjusted to fit the length of the path between points.

Let's now plot the profile and also a version of the profile created with
:func:`~bordado.profile_coordinates` for comparison:


.. jupyter-execute::

    # The spacing here is in degrees, but the path is not a great circle
    coordinates_wrong, _ = bd.profile_coordinates(
        são_paulo, luanda, spacing=1,
    )

    fig = pygmt.Figure()
    fig.coast(land="#cccccc", region="g", projection="G-20/0/20c", frame="afg")
    fig.plot(x=são_paulo[0], y=são_paulo[1], style="i0.5c", fill="seagreen", label="São Paulo")
    fig.plot(x=luanda[0], y=luanda[1], style="t0.5c", fill="orange", label="Luanda")
    fig.plot(x=coordinates[0], y=coordinates[1], pen="2p,slateblue2", label="Great circle")
    fig.plot(x=coordinates_wrong[0], y=coordinates_wrong[1], pen="2p,coral,-", label="Not great circle")
    fig.legend(position="jTR+l2p", box=pygmt.params.Box(fill="white"))
    fig.show()

We can clearly see in the plot that the two profiles take different paths, which
is why you should always use :func:`~bordado.great_circle_coordinates` when
dealing with longitude and latitude!


What's next
-----------

We can now create points along profiles with both Cartesian and geographic
coordinates! Another task you may have, particularly when sampling or generating
synthetic data, is to create a random spread of points. See how this can be done
with Bordado in ":ref:`tutorial_random`".

.. admonition:: Have questions?

    Please ask on any of the `Fatiando a Terra community channels
    <https://www.fatiando.org/contact>`__!

