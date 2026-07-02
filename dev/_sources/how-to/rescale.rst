.. _how_to_rescale:

Rescale coordinates to a different region
=========================================

Translating and stretching sets of points can sometimes be useful,
for example to produce synthetic data based on real data sampling.
This operation is basically rescaling a set of coordinates to a
different region (bounding box), and can be done with function
:func:`bordado.rescale_coordinates`.

.. jupyter-execute::

    import ensaio
    import pygmt
    import pandas as pd
    import bordado as bd

We'll use the Southern Africa gravity dataset as an example,
which is downloaded using :func:`ensaio.fetch_southern_africa_gravity`:

.. jupyter-execute::

    fname = ensaio.fetch_southern_africa_gravity(version=1)
    data = pd.read_csv(fname)
    data

Let's retrieve the original bounding box (region) of the data:

.. jupyter-execute::

    coordinates = (data.longitude, data.latitude)
    region = bd.get_region(coordinates)
    print(region)

And now we can plot the data along with coastlines so we can better
locate it:

.. jupyter-execute::

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="viridis",
        series=[data.gravity_mgal.min(), data.gravity_mgal.max()],
    )
    fig.plot(
        x=coordinates[0],
        y=coordinates[1],
        fill=data.gravity_mgal,
        cmap=True,
        style="c0.04c",
        projection="M15c",
        region=region,
    )
    fig.coast(
        shorelines=True,
        water="royalblue4",
        area_thresh=1e4,
        frame=["af", "+tOriginal data"],
    )
    fig.colorbar(frame=["af", "y+lmGal"])
    fig.show()

The dataset covers the entire Southern tip of Africa in point.
But let's say we want to translate it to the Amazon region of
South America and stretch in latitude a bit. To do so, we define
a new region and call :func:`~bordado.rescale_coordinates` like
so:

.. jupyter-execute::

    new_region = [-70, -50, -30, 10]
    rescaled = bd.rescale_coordinates(coordinates, new_region)
    print(rescaled)

The coordinates are now made to be contained in the ``new_region`` but
retaining relative positioning between them. Let's plot the rescaled
data on a map to visualize:

.. jupyter-execute::

    fig = pygmt.Figure()
    pygmt.makecpt(
        cmap="viridis",
        series=[data.gravity_mgal.min(), data.gravity_mgal.max()],
    )
    fig.plot(
        x=rescaled[0],
        y=rescaled[1],
        fill=data.gravity_mgal,
        cmap=True,
        style="c0.04c",
        projection="M15c",
        region=bd.pad_region(new_region, pad=(10, 5)),
    )
    fig.coast(
        shorelines=True,
        water="royalblue4",
        area_thresh=1e4,
        frame=["afg", "+tRescaled data"],
    )
    fig.colorbar(frame=["af", "y+lmGal"])
    fig.show()

Notice how the general survey layout is retained, but the coordinates
were translated to South America and stretch in latitude as desired.
