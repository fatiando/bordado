.. _tutorial_line:

Making evenly spaced values
===========================

.. jupyter-execute::

    import bordado as bd

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


