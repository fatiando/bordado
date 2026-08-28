.. _tutorial_line:

Making evenly spaced values
===========================

Generating arrays of evenly spaced values with :func:`bordado.line_coordinates`
is the most basic thing Bordado can do. It may seem trivial, but there are some
nuances to this. Let's see all the different ways it can be done.

.. jupyter-execute::

    import bordado as bd
    import numpy as np
    import matplotlib.pyplot as plt


Specifying the number of values
-------------------------------

Let's say we want to generate values between 0 and 10 with an interval of 0.5.
We can use function :func:`~bordado.line_coordinates` to do this by doing some
maths to figure out that we need 21 points for this (don't forget the extra one
because of the end point):

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, size=21)
    print(values)

Notice that the end points are always included. This should be pretty much
the same as using :func:`numpy.linspace`.


Specifying the spacing between values
-------------------------------------

Sometimes we want to specify the spacing between consecutive values instead of
the number of values.
We can do so by passing the ``spacing`` argument to :func:`~bordado.line_coordinates`
instead and let Bordado do the maths:

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, spacing=0.5)
    print(values)

Notice that, unlike :func:`numpy.arange`, the start and end values are
always included.


Adjusting spacing or boundaries
-------------------------------

The above example works well and could be reproduced with :func:`numpy.arange`
if the spacing is a multiple of the interval (here, we'll call the interval
the *region*). If it's not, then there's no way of fitting values inside
the region with the given spacing. In that case, we'll need to adjust the
region or the spacing.

Bordado will automatically adjust the spacing to make it fit the given region if
they are multiples:

.. jupyter-execute::

    values = bd.line_coordinates(0, 10, spacing=0.6)
    print(values)

This way, you can provide an approximate spacing that you desire without having
to calculate the exact spacing that would be a multiple of your interval.

If the spacing is important and must be preserved, we can ask Bordado do
adjust the region instead:

.. jupyter-execute::

    values_region = bd.line_coordinates(0, 10, spacing=0.6, adjust="region")
    print(values)

This same logic also applies to multidimensional sets of values or coordinates,
for example those belonging to :ref:`regular grids <tutorial_grid>`.

Let's make a quick plot of both sets of numbers so we can see what the
difference is:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(8, 3), layout="constrained")
    ax.plot(values, np.full_like(values, -1), "^")
    ax.plot(values_region, np.full_like(values_region, 1), "v")
    ax.set_ylim(-4, 4)
    ax.set_yticks([-1, 1])
    ax.set_yticklabels(["Spacing", "Region"])
    ax.set_xticks(np.arange(0, 10.01, 0.5))
    ax.grid(axis="x", linestyle="--")
    plt.show()

Pixel registration
------------------

We can also generate values at the middle of the intervals instead of at their
borders by passing the ``pixel_register`` argument:

.. jupyter-execute::

    values_pixel = bd.line_coordinates(0, 10, spacing=0.5, pixel_register=True)
    print(values_pixel)

    values = bd.line_coordinates(0, 10, spacing=0.5)
    print(values)

Notice that when using pixel-registration, there will be one less value because
we're calculating the number of intervals instead of the number of borders:

.. jupyter-execute::

    print(values.size, values_pixel.size)

Putting both arrays in a plot looks like this:

.. jupyter-execute::

    fig, ax = plt.subplots(1, 1, figsize=(8, 3), layout="constrained")
    ax.plot(values, np.full_like(values, -1), "^")
    ax.plot(values_pixel, np.full_like(values_pixel, 1), "v")
    ax.set_ylim(-4, 4)
    ax.set_yticks([-1, 1])
    ax.set_yticklabels(["Regular", "Pixel"])
    ax.set_xticks(np.arange(0, 10.01, 0.5))
    ax.grid(axis="x", linestyle="--")
    plt.show()

The logic for adjusting the region or the spacing remains the same for pixel
registration:


.. jupyter-execute::

    values_spacing = bd.line_coordinates(0, 10, spacing=0.6, pixel_register=True)
    print(values_spacing)
    print(values_spacing[1] - values_spacing[0])

    values_region = bd.line_coordinates(
        0, 10, spacing=0.6, pixel_register=True, adjust="region",
    )
    print(values_region)
    print(values_region[1] - values_region[0])

There is a slight rounding error but notice that the spacing is changed in the
first line while the region is changed in the second.

What's next
-----------

Now that you know how to make evenly spaced values in one dimension, let's see
how to apply that logic to multiple dimensions in ":ref:`tutorial_grid`".

.. admonition:: Have questions?

    Please ask on any of the `Fatiando a Terra community channels
    <https://www.fatiando.org/contact>`__!

