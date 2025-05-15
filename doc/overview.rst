.. _overview:

Overview
========

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

Checkout the ":ref:`api`" for a full list of all that Bordado offers.

Generating evenly spaced values
-------------------------------

Let's say we want to generate values between 0 and 10 with an interval of 0.5.
We can use function :func:`bordado.line_coordinates` to do this by doing some
maths to figure out that we need 21 points for this (don't forget the extra one
because of the end point):

.. jupyter-execute::

   values = bd.line_coordinates(0, 10, size=21)
   print(values)

Or we could pass the ``spacing`` argument to :func:`~bordado.line_coordinates`
instead and let Bordado do the maths:

.. jupyter-execute::

   values = bd.line_coordinates(0, 10, spacing=0.5)
   print(values)

We can also optionally generate values at the middle of the 0.5 wide cells
instead of at their borders by passing the ``pixel_register`` argument:

.. jupyter-execute::

   values_pixel = bd.line_coordinates(0, 10, spacing=0.5, pixel_register=True)
   print(values_pixel)

Notice that when using pixel-registration, there will be one less value because
we're calculating the number of intervals instead of the number of borders:

.. jupyter-execute::

   print(values.size, values_pixel.size)

Another benefit of using Bordado is that it will automatically adjust the
spacing to make it fit the given interval:

.. jupyter-execute::

   values = bd.line_coordinates(0, 10, spacing=0.6)
   print(values)

This way, you can provide an approximate spacing that you desire without having
to calculate the exact spacing that would be a multiple of your interval.
But if the spacing is important and must be preserved, we can ask Bordado do
adjust the interval (we call it a *region*) instead:

.. jupyter-execute::

   values = bd.line_coordinates(0, 10, spacing=0.6, adjust="region")
   print(values)

This same logic also applies to multidimensional sets of values or coordinates,
for example those belonging to regular grids.


Regular grids
-------------

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

Splitting into blocks
---------------------

Bordado has function :func:`bordado.block_split` that can provide indices for
segmenting coordinate arrays according to spatial blocks.
For example, let's make some random coordinates with
:func:`bordado.random_coordinates` and then divide them into blocks of a given
size:

.. jupyter-execute::

   coordinates = bd.random_coordinates(
       (20, 30, -50, -44), size=500, random_seed=42,
   )

.. note::

   The ``coordinates`` is a tuple with two 1d-arrays, one for each coordinate
   of our 2-dimensional region.

Then we can use :func:`~bordado.block_split` to get the indexers that split
these points into evenly sized blocks:

.. jupyter-execute::

   block_coordinates, labels = bd.block_split(coordinates, block_size=2)
   print(labels)

The labels are the number of the block to which each point belongs. For
example, these are the coordinates of the points that fall inside block 1:

.. jupyter-execute::

   for c in coordinates:
       print(c[labels==1])

The ``block_coordinates`` is a tuple with the coordinates of the center of each
block:

.. jupyter-execute::

   for c in block_coordinates:
       print(c)

Let's use :mod:`matplotlib` to plot this so we can understand it better. We'll
plot the block centers as stars and a scatter of the points colored according
to which block they belong:

.. jupyter-execute::

   import matplotlib.pyplot as plt

   fig, ax = plt.subplots(1, 1, figsize=(9, 5))
   tmp = ax.scatter(coordinates[0], coordinates[1], c=labels, cmap="tab20")
   fig.colorbar(tmp, label="Block number")
   ax.plot(block_coordinates[0], block_coordinates[1], "*k", markersize=10)
   plt.show()

.. seealso::

   The keen-eyed among you might have noticed that the coordinates of the block
   centers are **not spaced by 2** (the block size). This is because by default
   :func:`~bordado.block_split` extracts the region that is divided into blocks
   from the input data, which are random and there are no points exactly on the
   region boundaries. You can pass a ``region`` argument to make this be exact
   if desired.

Explore the rest!
-----------------

That's a brief overview of the functionality in Bordado but there's plenty
more! Have a look at the ":ref:`api`" and the documentation for each function.

If you have any questions, please ask on any of the `Fatiando a Terra community
channels <https://www.fatiando.org/contact>`__! We're also always looking for
more people to get involved in the development. Leave us a message if that's
you.

Oh, and don't forget to :ref:`cite Bordado <citing>` if you use it in
a publication!
