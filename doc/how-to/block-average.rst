.. _how_to_block_average:

Calculate data averages in blocks
=================================

.. jupyter-execute::

    import ensaio
    import pyproj
    import pygmt
    import pandas as pd
    import bordado as bd

.. jupyter-execute::

    fname = ensaio.fetch_sierra_negra_topography(version=1)
    data = pd.read_csv(fname)
    region = bd.get_region((data.longitude, data.latitude))
    data

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
        frame=True,
    )
    fig.colorbar(frame='af+ltopography [m]')
    fig.show()

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    easting, northing = projection(data.longitude, data.latitude)

.. jupyter-execute::

    block_coordinates, labels = bd.block_split(
        coordinates=(easting, northing),
        block_size = 2,
    )
    data["block_id"] = labels
    data

.. jupyter-execute::

    block_data = data.groupby("block_id").mean()
    block_data

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
        style="c0.05c",
        projection="M15c",
        region=region,
        frame=True,
    )
    fig.colorbar(frame='af+ltopography [m]')
    fig.show()
