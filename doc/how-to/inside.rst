.. _how_to_inside:

Select points that fall inside a region
=======================================

When we have irregularly sampled data, it can be tedious to select the
points that fall inside a given region (bounding box). It can be done with
:mod:`numpy` or :mod:`pandas` boolean indexing, of course. But Bordado offers
:func:`bordado.inside` to make this easier and generalizable to n-dimensions.
Let's see how it works on a real dataset!

.. jupyter-execute::

    import ensaio
    import pygmt
    import pandas as pd
    import bordado as bd

We'll use :func:`ensaio.fetch_caribbean_bathymetry` to fetch some bathymetry
data from the Caribbean. The dataset is a CSV file, which can be loaded with
:func:`pandas.read_csv`:

.. jupyter-execute::

    fname = ensaio.fetch_caribbean_bathymetry(version=2)
    data = pd.read_csv(fname)
    data

Let's plot the data with :mod:`pygmt` to see what we've got:

.. jupyter-execute::

    region = bd.get_region((data.longitude, data.latitude))

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="cmocean/topo+h",
        series=[data.bathymetry_m.min(), data.bathymetry_m.max()],
    )
    fig.plot(
        x=data.longitude,
        y=data.latitude,
        fill=data.bathymetry_m,
        cmap=True,
        style="c0.02c",
        projection="M15c",
        region=region,
        frame=True,
    )
    fig.colorbar(frame='af+l"bathymetry [m]"')
    fig.coast(land="#666666")
    fig.show()

Now, let's say we wanted only the data that around `Barbados
<https://en.wikipedia.org/wiki/Barbados>`__. We may have the exact region that
we want to crop the data:

.. jupyter-execute::

    region_barbados = (-60.3, -58.7, 12.5, 13.7)  # W, E, S, N

We can use :func:`bordado.inside` to get an index for our dataset that will
select only data inside the given region:

.. jupyter-execute::

    barbados = bd.inside(
        coordinates=(data.longitude, data.latitude),
        region=region_barbados,
    )
    barbados

With the index, we can select the data like so:

.. jupyter-execute::

    data_barbados = data[barbados]
    data_barbados

And plot the selected data:

.. jupyter-execute::

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="cmocean/topo+h",
        series=[
            data_barbados.bathymetry_m.min(),
            data_barbados.bathymetry_m.max(),
        ],
    )
    fig.plot(
        x=data_barbados.longitude,
        y=data_barbados.latitude,
        fill=data_barbados.bathymetry_m,
        cmap=True,
        style="c0.02c",
        projection="M15c",
        region=region,
        frame=True,
    )
    fig.colorbar(frame='af+l"bathymetry [m]"')
    fig.coast(land="#666666")
    fig.show()

.. hint::

    The order of the coordinates must be the same as the order of elements in
    the region. If the region is W, E, S, N, then the coordinates must be
    longitude and then latitude.
