.. _how_to_rolling_average:

Calculate a rolling average of scattered point data
===================================================

Rolling averages are great for smoothing and downsampling data. It's relatively
easy to perform them on regularly spaced data but not so for scattered points.
Let's see how we can use :func:`bordado.rolling_window` to calculate a rolling
average of some scattered topography data.

.. jupyter-execute::

    import ensaio
    import pyproj
    import pygmt
    import numpy as np
    import pandas as pd
    import xarray as xr
    import bordado as bd

For this example, we'll use :func:`ensaio.ensaio.fetch_sierra_negra_topography`
to get some topography data from the Sierra Negra volcano in the Galapagos:

.. jupyter-execute::

    fname = ensaio.fetch_sierra_negra_topography(version=1)
    data = pd.read_csv(fname)
    data

Let's plot the data with :mod:`pygmt` to see what we've got:

.. jupyter-execute::

    region = bd.get_region((data.longitude, data.latitude))
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
        frame="afg",
    )
    fig.colorbar(frame=["af+lOriginal topography", "y+lm"])
    fig.show()

The data are very high resolution and dense. If we want to smooth it and
downsample it, a rolling average is just what we need.

Let's first project the data so we can work with Cartesian distances instead
of angles:

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    easting, northing = projection(data.longitude, data.latitude)

Now we can call :func:`~bordado.rolling_windows` to split the data into 5 meter
windows with a 75% overlap:

.. jupyter-execute::

    coordinates_proj, indices = bd.rolling_window(
        (easting, northing), window_size=5, overlap=0.75,
    )
    # Get back longitude and latitude for the center of each window
    coordinates = projection(*coordinates_proj, inverse=True)

With this, we have the coordinates of the center of each window and the indices
of the data points that fall inside each window. To calculate the rolling
average, we iterate over the ``indices`` and use them to index the data:

.. jupyter-execute::

    average_values = np.empty_like(coordinates[0])
    for i in range(indices.shape[0]):
        for j in range(indices.shape[1]):
            average_values[i, j] = np.mean(data.elevation_m.iloc[indices[i, j]])
    average_values

If we choose to assign the data values to the coordinates of the center of the
windows, we now have a regular grid. We can wrap the coordinates and the rolling
average in a :class:`xarray.DataArray`:

.. jupyter-execute::

    average = xr.DataArray(
        average_values,
        coords={"longitude": coordinates[0][0, :], "latitude": coordinates[1][:, 0]},
        dims=("latitude", "longitude")
    )
    average

.. note::

    While it's useful to have a :class:`xarray.DataArray`, this step is entirely
    optional.

The :class:`~xarray.DataArray` can be passed to :meth:`pygmt.Figure.grdimage` to
make a pseudo-color plot of the smoothed topography with some hill shading:

.. jupyter-execute::

    fig = pygmt.Figure()
    fig.grdimage(
        average,
        cmap="viridis",
        projection="M15c",
        region=region,
        shading=True,
        frame="afg",
    )
    fig.colorbar(frame=["af+l5 meter mean topography", "y+lm"])
    fig.show()

The features in the 5-meter average grid above are smoothed when compared to the
original point data.
