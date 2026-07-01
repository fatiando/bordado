.. _how_to_block_average:

Calculate data averages in blocks
=================================

Point or line data can often be oversampled, for example along flight lines or
ship tracks, or unevenly sampled across the data region. This can be undesired
for plotting or lead to biases in interpolation and other analyses. A safe way
to reduce (downsample) the data without causing
`aliasing <https://en.wikipedia.org/wiki/Aliasing>`__ is to divide the data into
blocks and then take the mean or other statistic of the points that fall inside
each block. We'll demonstrate how to do this with :func:`bordado.block_split`
and :mod:`pandas`.

.. jupyter-execute::

    import ensaio
    import pyproj
    import pygmt
    import pandas as pd
    import bordado as bd

First, let's get some topography data that we can use for this example
through :func:`ensaio.fetch_british_columbia_lidar`:

.. jupyter-execute::

    fname = ensaio.fetch_british_columbia_lidar(version=1)
    data = pd.read_csv(fname)
    data

This is a LIDAR dataset from a few islands in British Columbia, Canada.
Let's use :func:`bordado.get_region` and :func:`bordado.pad_region` to
extract the data bounding box and pad it a little. This will be useful
to make plots of the data without having the plot margins directly
touching the data.

.. jupyter-execute::

    region = bd.pad_region(
        bd.get_region((data.longitude, data.latitude)),
        pad=(5 / 3600, 3 / 3600),
    )
    region

Let's plot the data with :mod:`pygmt` to see what we've got:

.. jupyter-execute::

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="viridis",
        series=[data.elevation_m.min(), data.elevation_m.max()],
    )
    fig.plot(
        x=data.longitude,
        y=data.latitude,
        fill=data.elevation_m,
        cmap=True,
        style="c0.01c",
        projection="M15c",
        region=region,
        frame=["afg", "+tOriginal topography"],
    )
    fig.colorbar(frame=["af", "y+lm"])
    fig.show()

Notice that the sampling is not uniform, with areas of denser sampling
and areas with no points at all.

The dataset is in geodetic longitude and latitude coordinates so we
should first project it so we can use the regular Cartesian distance
calculations in :func:`~bordado.block_split`:

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    easting, northing = projection(data.longitude, data.latitude)

Now we can divide the data into 2 meter blocks. The ``labels`` variable
contains the index of the block to which each point belongs.

.. jupyter-execute::

    block_coordinates, labels = bd.block_split(
        coordinates=(easting, northing),
        block_size = 2,
    )
    data["block_id"] = labels
    data

Our dataset now contains the block indices (IDs) for each point.
To do a reduction operation (like mean, median, standard deviation, sum, etc),
we can use the :meth:`pandas.DataFrame.groupby` method:

.. jupyter-execute::

    block_data = data.groupby("block_id").mean()
    block_data

This new dataset has the mean longitude, latitude, and elevation per 2 meter
block. The reduced dataset looks like this:

.. jupyter-execute::

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="viridis",
        series=[data.elevation_m.min(), data.elevation_m.max()],
    )
    fig.plot(
        x=block_data.longitude,
        y=block_data.latitude,
        fill=block_data.elevation_m,
        cmap=True,
        style="c0.01c",
        projection="M15c",
        region=region,
        frame=["afg", "+tBlock average topography"],
    )
    fig.colorbar(frame=["af", "y+lm"])
    fig.show()

Notice that now the points are more uniformly spaced and there are no
areas with much higher point density.

.. seealso::

    This is how the :class:`verde.BlockReduce` class works!
