.. _overview:

Why use Bordado?
================

The main purpose of Bordado is to facilitate **generating coordinates for
evenly spaced points**.
These could be the coordinates of a regular grid, of points along a line, or of
a profile.
While you could do a lot of this with a combination of :func:`numpy.linspace`
and :func:`numpy.meshgrid`, there are a few problems that Bordado solves:

1. What if I want to specify the spacing between points instead of how many
   points?
2. What if the spacing isn't exactly a multiple of the interval?
3. What was the order of arguments to :func:`numpy.meshgrid` and what's the
   difference between the difference indexing types?
4. What if I want points along a straight line or great circle between two
   points?

On top of that, Bordado also offers other utilities like splitting points into
blocks and rolling windows, calculating some nearest neighbor statistics, and
more.

**Let's see how it works!**

Importing the package
---------------------

Everything in Bordado is available through the :mod:`bordado` module. There are
no submodules to import. We'll usually alias the import to ``bd``:

.. jupyter-execute::

    import bordado as bd

.. tip::

    Checkout the ":ref:`api`" for a full list of all that Bordado offers.

We'll also import :mod:`numpy` to use for some comparisons.

.. jupyter-execute::

    import numpy as np


Generating evenly spaced points
-------------------------------

As a first taste, let's see how to generate values between two extremes, but
passing the spacing between values instead of the number of values:

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, spacing=1)
    print(values)

Notice how both extremes are included, contrasting with :func:`numpy.arange`:

.. jupyter-execute::

    values_arange = np.arange(0, 10, 1)
    print(values_arange)

Another nice thing is that :func:`~bordado.line_coordinates` will round the
spacing if it's not a multiple of the interval, guaranteeing that the
interval boundaries are always present:

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, spacing=1.3)
    print("Bordado:", values)

    values_arange = np.arange(0, 10, 1.3)
    print("Numpy:", values_arange)

We can also ask it to adjust the interval instead of the spacing:

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, spacing=1.3, adjust="region")
    print(values)

The same logic applies to regular grids with :func:`bordado.grid_coordinates`,
which generates the values and uses :func:`numpy.meshgrid` appropriately:

.. jupyter-execute::

    x, y = bd.grid_coordinates(region=(0, 10, 10, 20), spacing=1.3)
    print(x)
    print(y)


Explore the rest!
-----------------

That's a brief overview of the functionality in Bordado but there's plenty
more! We recommend going through our tutorial first, starting at
":ref:`tutorial_line`".
Then take a look at the ":ref:`api`" and the documentation for each function.

Oh, and don't forget to :ref:`cite Bordado <citing>` if you use it in
a publication!

.. admonition:: Have questions?

    Please ask on any of the `Fatiando a Terra community channels
    <https://www.fatiando.org/contact>`__! We're also always looking for
    feedback and more people to get involved in the development. Leave us a
    message if that's you.
