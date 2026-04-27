.. _tutorial_split:

Splitting points into blocks
============================


Non-overlapping spatial blocks
------------------------------



Selecting points inside expanding windows
-----------------------------------------


Splitting points into rolling windows
-------------------------------------


Rolling windows on the sphere
-----------------------------

.. jupyter-execute::

    import bordado as bd

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
