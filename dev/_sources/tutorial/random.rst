.. _tutorial_random:

Random coordinates
==================

Sometimes, we need to generate a random spread of points in 1 or more
dimensions. This can be used for random sampling methods or simply to
generate some synthetic data on which to test new methods. Generating
uniformly distributed values using :mod:`numpy.random` is great but doing
so in more than 1 dimension involves some boilerplate code that  could be
automated. Bordado offers functions :func:`~bordado.random_coordinates` and
:func:`~bordado.random_coordinates_spherical` for this purpose. This is how they
work.

.. jupyter-execute::

    import bordado as bd
    import matplotlib.pyplot as plt
    import pygmt


Generating random points
------------------------

To generate uniformly distributed random 2D point coordinates, we use :func:`bordado.random_coordinates` like so:

.. jupyter-execute::

    region = (0, 20, -45, -30)
    coordinates = bd.random_coordinates(region, size=50)

    for i, c in enumerate(coordinates):
        print(f"coordinate {i}:\n{c}\n")

Since the ``region`` has 4 elements, it is assumed that there are two dimensions
in our problem and so 2 coordinates arrays are generated. Because the points are
uniformly distributed, there is only a ``size`` argument and no spacing like in
:func:`bordado.grid_coordinates` or :func:`bordado.line_coordinates`.

.. hint::

    The values above will be different every time we run the function because
    it will instantiate a new :func:`numpy.random.default_rng` every time. We
    can control the randomness by passing a ``random_seed`` argument. This can
    be an integer seed or a :class:`numpy.random.Generator`.

Let's plot these points to see their distribution:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(8, 6), layout="constrained")
    ax.plot(*coordinates, "o")
    ax.set_aspect("equal")
    ax.set_xlim(*region[:2])
    ax.set_ylim(*region[2:])
    ax.set_xlabel("Easting")
    ax.set_ylabel("Northing")
    ax.grid()
    plt.show()

As expected, they are random and with no bias inside the given region (hence,
uniformly distributed).


Random points on the sphere
---------------------------

The method above is useful, but it shouldn't be used with geographic longitude and latitude coordinates. Let's illustrate why with an example. We'll generate random points distributed globally:

.. jupyter-execute::

    region = (0, 360, -90, 90)  # W, E, S, N in degrees
    size = 3000

    coordinates = bd.random_coordinates(region, size)

    fig, ax = plt.subplots(1, 1, figsize=(8, 6), layout="constrained")
    ax.plot(*coordinates, ".")
    ax.set_aspect("equal")
    ax.set_xlim(*region[:2])
    ax.set_ylim(*region[2:])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid()
    plt.show()

Plotted like this, things seem fine. But this type of plot can be very misleading for geographic data.
If I plot them on a map using a cartographic projection, a pattern will appear:

.. jupyter-execute::

    fig = pygmt.Figure()
    fig.coast(land="#cccccc", region="g", projection="W20c", frame="afg")
    fig.plot(x=coordinates[0], y=coordinates[1], style="c0.1c", fill="seagreen")
    fig.show()

Now we can see that the concentration of points is larger at the poles than at
the equator. This is because the meridians of longitude converge at the poles.
Hence, a degree of longitude corresponds to a smaller and smaller physical size
on the surface of the Earth towards the poles.

.. seealso::

    The map above was generated with a `Mollweide projection
    <https://en.wikipedia.org/wiki/Mollweide_projection>`__, which is an
    equal-area projection.

To generate random points on a sphere that have a uniform distribution, we
can use :func:`bordado.random_coordinates_spherical`, which accounts for this
convergence of meridians:

.. jupyter-execute::

    coordinates_sphere = bd.random_coordinates_spherical(region, size)

    fig = pygmt.Figure()
    fig.coast(land="#cccccc", region="g", projection="W20c", frame="afg")
    fig.plot(x=coordinates_sphere[0], y=coordinates_sphere[1], style="c0.1c", fill="seagreen")
    fig.show()

Notice that now the point concentration is uniform on the Earth.


What's next
-----------

Now that we can make some synthetic data with random points, let's see how
we can split and segment the data based on spatial blocks and windows in
":ref:`tutorial_split`".

.. admonition:: Have questions?

    Please ask on any of the `Fatiando a Terra community channels
    <https://www.fatiando.org/contact>`__!

