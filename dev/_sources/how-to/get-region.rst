.. _how_to_get_region:

Get the region (bounding box) of a set of points
================================================

Let's say we have a dataset that has longitude and latitude coordinates (but
it could also be whatever other type of coordinate). And we need to know the
bounding box of this dataset, which we call a *region*, comprised of West, East,
South, and North values. Bordado offers :func:`bordado.get_region` to do this.

.. jupyter-execute::

    import ensaio
    import pandas as pd
    import bordado as bd

To demonstrate, we'll use :func:`ensaio.fetch_southern_africa_gravity` to get a
sample dataset of ground-based gravity observation across Southern Africa. The
dataset is a CSV file, which we'll load using :func:`pandas.read_csv`:

.. jupyter-execute::

    fname = ensaio.fetch_southern_africa_gravity(version=1)
    data = pd.read_csv(fname)
    data

We can then use :func:`~bordado.get_region` to extract the bounding box
information:

.. jupyter-execute::

    coordinates = (data.longitude, data.latitude)
    region = bd.get_region(coordinates)
    print(region)

The ``region`` above will have the minimum and maximum values of each coordinate
in order. The order of the coordinates will be the order of the output region.
In this case, the numbers correspond to the West and East longitude, followed by
the South and North latitude.

.. note::

    We tend to always use "longitude" or "easting" and then "latitude" or
    "northing" as the order of coordinates. But Bordado can work with whatever
    order you choose:

    .. jupyter-execute::

        coordinates = (data.latitude, data.longitude)
        region = bd.get_region(coordinates)
        print(region)

    Just be aware of your own conventions.

If the ``height_sea_level_m`` column is considered another coordinate
and we want the 3D bounding box, we can pass more than 2 values to
:func:`~bordado.get_region`:

.. jupyter-execute::

    coordinates_3d = (data.longitude, data.latitude, data.height_sea_level_m)
    region_3d = bd.get_region(coordinates_3d)
    print(region_3d)

In this case, the minimum and maximum height are the two last values of the
``region_3d`` tuple.
