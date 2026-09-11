.. how_to_median_distance:

Calculate the median distance between points
============================================

With irregularly sampled data, it can be useful to get some statistics about
the distances between points. This can be used to determine grid spacing, point
density calculations, and other useful things.
Bordado offers function :func:`bordado.neighbor_distance_statistics` to do these
calculations.
Let's use it on a real dataset to calculate the median distance between
neighboring points.

.. jupyter-execute::

    import ensaio
    import pygmt
    import pyproj
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import bordado as bd

We'll use :func:`ensaio.fetch_sierra_negra_topography` to download a topography
dataset of the Sierra Negra volcano on the Galápagos. We'll then load the data
into memory using :func:`pandas.read_csv`:

.. jupyter-execute::

    fname = ensaio.fetch_sierra_negra_topography(version=1)
    data = pd.read_csv(fname)
    data

Let's plot the data with :mod:`pygmt` to see what we've got:

.. jupyter-execute::

    region = bd.get_region((data.longitude, data.latitude))

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="cmocean/topo+h",
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
    fig.colorbar(frame=["af+lElevation", "y+lm"])
    fig.show()

The distance calculations will be Cartesian by default so we must first project the geographic coordinates using :mod:`pyproj`:

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    coordinates = projection(data.longitude, data.latitude)

Function :func:`~bordado.neighbor_distance_statistics` will calculate the
distances to the ``k`` nearest neighbors of all points and then run a statistic
(mean, median, standard deviation, etc) on these ``k`` distances.
For example, we can calculate the median distance to each points 3 nearest neighbors:

.. jupyter-execute::

    distances = bd.neighbor_distance_statistics(coordinates, "median", k=3)
    print(distances)

It can be helpful to plot a histogram of these distances to see the degree of
uniformity of our dataset:

.. jupyter-execute::

    plt.figure(figsize=(8, 5))
    plt.hist(distances, bins=50)
    plt.xlabel("Median distance to 3 nearest neighbors (m)")
    plt.ylabel("Number of occurrences")
    plt.show()

The distribution is not normal and seems to have some peaks. Nonetheless,
the median of these distances can be a good summary of how close the points are:

.. jupyter-execute::

    median_distance = np.median(distances)
    print(f"Median distance between points: {median_distance:.2f} m")

This measure can be useful for determining a grid size for interpolation, for
example.
