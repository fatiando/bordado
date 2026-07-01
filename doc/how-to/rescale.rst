.. _how_to_rescale:

Rescale coordinates to a different region
=========================================

.. jupyter-execute::

    import ensaio
    import pygmt
    import pandas as pd
    import bordado as bd

.. jupyter-execute::

    fname = ensaio.fetch_southern_africa_gravity(version=1)
    data = pd.read_csv(fname)
    data

.. jupyter-execute::

    coordinates = (data.longitude, data.latitude)
    region = bd.get_region(coordinates)
    print(region)

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


.. jupyter-execute::

    new_region = [-70, -50, -30, 10]
    rescaled = bd.rescale_coordinates(coordinates, new_region)

.. jupyter-execute::

    plot_region = [-90, 40, -40, 15]
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
        style="c0.01c",
        projection="M15c",
        region=plot_region,
    )
    fig.plot(
        x=rescaled[0],
        y=rescaled[1],
        fill=data.gravity_mgal,
        cmap=True,
        style="c0.01c",
    )
    fig.coast(
        shorelines=True,
        water="royalblue4",
        area_thresh=1e4,
        frame=["af", "+tOriginal and rescaled data"],
    )
    fig.colorbar(frame=["af", "y+lmGal"])
    fig.show()
