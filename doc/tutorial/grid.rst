.. _tutorial_grid:

Coordinates for regular grids
=============================

.. jupyter-execute::

    import bordado as bd

Function :func:`bordado.grid_coordinates` combines
:func:`~bordado.line_coordinates` to generate sets of coordinates for grids.
For example, this is how we generate coordinates for a 2D grid:

.. jupyter-execute::

    coordinates = bd.grid_coordinates((0, 10, -5, 5), spacing=2)
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:")
       print(c)

The first argument to :func:`~bordado.grid_coordinates` is called a **region**
in Bordado and it specifies the boundaries of the domain which contains the
grid.

.. hint::

    The **region** will always have an even number of elements. Each pair is the
    minimum and maximum value along a dimension of the grid. In our example, the
    first coordinate is between 0 and 10 and the send between -5 and 5.

The coordinates are returned as a :class:`tuple` of numpy arrays that have
dimensions compatible with the number of elements in the region.
We can make multidimensional grids by adding more elements to the region:

.. jupyter-execute::

    coordinates = bd.grid_coordinates((0, 9, -3, 3, 6, 12), spacing=3)
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:")
       print(c)
       print()

Just like with :func:`~bordado.line_coordinates`, we can pass a spacing that
isn't exactly a multiple of the dimensions of the region:

.. jupyter-execute::

    coordinates = bd.grid_coordinates((0, 10, -5, 5), spacing=2.6)
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:")
       print(c)

And we can also adjust the region instead of the spacing:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(
       (0, 10, -5, 5), spacing=2.6, adjust="region",
    )
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:")
       print(c)

Bordado also offers a lot more than generating coordinates. Let's see how we
can use it to split points as well.
