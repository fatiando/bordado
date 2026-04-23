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
    import matplotlib.pyplot as plt


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
       print(f"coordinate {i} (shape = {c.shape}):\n{c}\n")

The order of the arguments is the same as for the ``spacing``. Notice that the
shape of the coordinate arrays is the same as the input shape.


Automatic adjustment of spacing or region
-----------------------------------------

Just like with :func:`~bordado.line_coordinates`, we can pass a spacing that
isn't exactly a multiple of the dimensions of the region. In this case, the
spacing will be automatically adjusted to fit the given region exactly:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(region=(0, 10, -5, 5), spacing=2.6)

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")

This is very useful when the exact spacing is not too important, but the
boundaries of the region must be preserved.
If the boundaries aren't important, but the exact spacing is, we can also ask
:func:`~bordado.grid_coordinates` to adjust the region instead of the spacing:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(
       region=(0, 10, -5, 5), spacing=2.6, adjust="region",
    )

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")

.. admonition:: When to ``adjust="region"``?
    :class: note

    If the boundaries are important (for example, longitude should not be more
    than 360), then ``adjust="spacing"`` (the default). But in this case the
    spacing may not be exactly what you asked for.

    If the exact spacing is important, but the boundaries are not, then
    ``adjust="region"``.

Let's visualize the difference between these two types of adjustment:

.. jupyter-execute::

    region = (0, 10, -5, 5)
    spacing = 2.6
    coords_spacing = bd.grid_coordinates(region, spacing=spacing)
    coords_region = bd.grid_coordinates(region, spacing=spacing, adjust="region")

    def plot_region(ax, region):
        "Plot the region as a solid line."
        west, east, south, north = region
        ax.add_patch(
            plt.Rectangle(
                (west, south),
                east - west,
                north - south,
                fill=None,
                label="Region bounds",
            )
        )

    def plot_grid(ax, coordinates, linestyles="dotted", region=None, pad=50, **kwargs):
        "Plot the grid coordinates as dots and lines."
        data_region = bd.get_region(coordinates)
        ax.vlines(
            coordinates[0][0],
            ymin=data_region[2],
            ymax=data_region[3],
            linestyles=linestyles,
            zorder=0,
        )
        ax.hlines(
            coordinates[1][:, 1],
            xmin=data_region[0],
            xmax=data_region[1],
            linestyles=linestyles,
            zorder=0,
        )
        ax.scatter(*coordinates, **kwargs)

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111)
    plot_region(ax, region)
    plot_grid(
        ax=ax,
        coordinates=coords_region,
        region=region,
        label="Adjusted Region Grid Nodes",
        marker=">",
        color="blue",
        alpha=0.75,
        s=100,
    )
    plot_grid(
        ax=ax,
        coordinates=coords_spacing,
        region=region,
        label="Adjusted Spacing Grid Nodes",
        marker=">",
        color="orange",
        alpha=0.75,
        s=100,
    )
    ax.set_xlabel("Easting")
    ax.set_ylabel("Northing")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18))
    plt.show()



Pixel registration
------------------

We can also generate coordinate values at the center of the intervals instead
of at their borders (the default) by passing ``pixel_register=True``:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(
        region=(0, 10, -5, 5), spacing=2, pixel_register=True,
    )

    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")

Notice that the region boundary values aren't included, and the first and last
coordinates are half of the spacing away from the boundaries.



Multidimensional grids and meshes
---------------------------------

We can make multidimensional grids by adding more elements to the region:

.. jupyter-execute::

    coordinates = bd.grid_coordinates((0, 9, -3, 3, 6, 12), spacing=3)
    for i, c in enumerate(coordinates):
       print(f"coordinate {i}:\n{c}\n")
