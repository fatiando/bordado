.. _how_to_pad_region:

Extend a region on all sides
============================

Sometimes, we have the values of a region (bounding box) that contains our data
and need to pad it on all sides for some reason. This could be the boundaries of
a plot or map that we're making, or a larger region of influence that needs to
be considered, or something else. Bordado offers :func:`bordado.pad_region` to
do this for you in n-dimensions.

.. jupyter-execute::

    import ensaio
    import pygmt
    import pandas as pd
    import bordado as bd

Let's illustrate this using a  sample dataset of ground-based
gravity observations across Southern Africa which we'll download with
:func:`ensaio.fetch_southern_africa_gravity` and open with :func:`pandas.read_csv`:

.. jupyter-execute::

    fname = ensaio.fetch_southern_africa_gravity(version=1)
    data = pd.read_csv(fname)
    data

We can then use :func:`~bordado.get_region` to find the exact bounding box
of the data:

.. jupyter-execute::

    coordinates = (data.longitude, data.latitude)
    region = bd.get_region(coordinates)
    print(region)

If we plot the data using this bounding box, it may not look very good since
some data points will be exactly at the boundary. Let's make a quick map of the
point locations with :mod:`pygmt` and the ``region`` that we found above:

.. jupyter-execute::

    fig = pygmt.Figure()
    fig.coast(region=region, projection="M20c", land="#cccccc", frame=True)
    fig.plot(x=data.longitude, y=data.latitude, style="c0.1c", fill="maroon")
    fig.show()

The points are where we have data. But when we use the exact region, the map
boundaries are touching some of the points, making it more difficult to see them
all. The map would be better if we padded the region a bit on all sides. Let's
add some padding of 1.5° to each side using :func:`~bordado.pad_region`:

.. jupyter-execute::

    region_pad = bd.pad_region(region, pad=1.5)
    print("Original:", region)
    print("Padded:", region_pad)

Now let's make a new map with the padded region:

.. jupyter-execute::

    fig = pygmt.Figure()
    fig.coast(region=region_pad, projection="M20c", land="#cccccc", frame=True)
    fig.plot(x=data.longitude, y=data.latitude, style="c0.1c", fill="maroon")
    fig.show()

That's better! Now we can see the full outline of the survey.
