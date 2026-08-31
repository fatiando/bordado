.. _how_to_median_distance:

Calculate median distances between points
=========================================

Knowing the typical spacing between neighboring data points is useful when
choosing grid spacings, window sizes, or interpolation parameters. Bordado
offers :func:`bordado.neighbor_distance_statistics` to calculate statistics of
nearest-neighbor distances for a set of points. Let's use it to estimate the
median spacing in a real dataset.

.. jupyter-execute::

    import ensaio
    import pyproj
    import numpy as np
    import pandas as pd
    import bordado as bd

We'll use :func:`ensaio.fetch_southern_africa_gravity` to fetch some
ground-based gravity observations from Southern Africa and load them with
:func:`pandas.read_csv`:

.. jupyter-execute::

    fname = ensaio.fetch_southern_africa_gravity(version=1)
    data = pd.read_csv(fname)
    data

The data coordinates are longitudes and latitudes in degrees. Since the
nearest-neighbor distances calculated by Bordado are Cartesian distances, we
should project them to a coordinate system in meters first:

.. jupyter-execute::

    projection = pyproj.Proj(proj="merc", lat_ts=data.latitude.mean())
    coordinates = projection(data.longitude, data.latitude)

Now we can calculate the distance from each point to its nearest neighbor by
using the ``"median"`` statistic with ``k=1``:

.. jupyter-execute::

    nearest_neighbor = bd.neighbor_distance_statistics(
        coordinates,
        "median",
        k=1,
    )
    print(nearest_neighbor)

The median of these nearest-neighbor distances gives a single estimate of the
typical spacing between points:

.. jupyter-execute::

    spacing = np.median(nearest_neighbor)
    print(f"Median nearest-neighbor distance: {spacing / 1000:.2f} km")

For datasets sampled along survey lines, the closest neighbor may be on the
same line and much closer than points on neighboring lines. In these cases,
using more neighbors can give a more representative value:

.. jupyter-execute::

    for k in [1, 3, 5, 10]:
        distances = bd.neighbor_distance_statistics(coordinates, "median", k=k)
        spacing = np.median(distances)
        print(f"k={k:2d}: {spacing / 1000:.2f} km")

The best value of ``k`` depends on the sampling pattern of your data and the
scale of the process that you want to resolve.
