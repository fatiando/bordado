.. _tutorial_grid:

Coordinates for regular grids and meshes
========================================

Now that we learned how to make evenly spaced values with
:func:`bordado.line_coordinates`, we could use :func:`numpy.meshgrid` to
generate multidimensional arrays of values for things like coordinates of
regular grids and regular meshes. However, there are a few important details
that may be overlooked when doing so. Bordado can handle all of this for us
using function :func:`bordado.grid_coordinates`. Let's see how it's used to make
coordinates for regular grids in 2 or more dimensions.

.. jupyter-execute::

    import bordado as bd


Coordinates for 2D grids
------------------------

Function :func:`bordado.grid_coordinates` combines
:func:`~bordado.line_coordinates` to generate sets of coordinates for grids.
For example, this is how we generate coordinates for a 2D grid:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(region=(0, 10, -5, 5), spacing=2)

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")

The first argument to :func:`~bordado.grid_coordinates` is called a **region**
in Bordado. It specifies the boundaries of the domain which contains the
grid. The number of elements in the region specifies the number of dimensions
of the output. There should be 2 values in the region per dimension of the grid.
So 4 values in ``region`` means we're making a 2D grid. Hence, a :class:`tuple`
of two 2D numpy arrays with the coordinates is returned.

.. admonition:: What is a region?
    :class: hint

    The **region** will always have an even number of elements. Each pair is the
    minimum and maximum value along a dimension of the grid. In our example, the
    first coordinate is between 0 and 10 and the second between -5 and 5. For
    geographic coordinates (longitude, latitude), the region would represent
    the **west, east, south, and north** boundaries of the domain.

We can also specify different spacings for each dimension of the grid by passing
a tuple or list as the ``spacing`` argument:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(region=(0, 10, -5, 5), spacing=(2.5, 2))

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")

The order of the ``spacing`` argument is the **reversed order of the arguments in
the region**. This is done for compatibility with how numpy specifies the ``shape``
parameter of arrays.

Speaking of which, we can also specify the shape of the desired coordinate arrays
instead of the spacing:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(region=(0, 10, -5, 5), shape=(6, 11))

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")


Automatic adjustment of spacing or region
-----------------------------------------

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


Multidimensional grids and meshes
---------------------------------

We can make multidimensional grids by adding more elements to the region:

.. jupyter-execute::

    coordinates = bd.grid_coordinates((0, 9, -3, 3, 6, 12), spacing=3)
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:")
       print(c)
       print()
