.. _install:

Installing
==========

Which Python?
-------------

You'll need **Python 3.9 or greater**.
See :ref:`python-versions` if you require support for older versions.


Dependencies
------------

The required dependencies should be installed automatically when you install
Bordado using ``conda`` or ``pip``. Optional dependencies have to be
installed manually.

.. note::

    See :ref:`dependency-versions` for the our policy of oldest supported
    versions of each dependency.

Required:

* `numpy <http://www.numpy.org/>`__
* `scipy <https://https://docs.scipy.org/doc/scipy/>`__

The examples in documentation also use:

* `matplotlib <https://matplotlib.org/>`__ for plotting

Installing with conda
---------------------

You can install Bordado using the `conda package manager
<https://conda.io/>`__ that comes with the Anaconda distribution::

    conda install bordado --channel conda-forge

.. tip::

   We recommend using the
   `Miniforge distribution <https://conda-forge.org/download/>`__
   to ensure that you have the ``conda`` package manager available.
   Installing Miniforge does not require administrative rights to your computer
   and doesn't interfere with any other Python installations in your system.
   It's also much smaller than the Anaconda distribution and is less likely to
   break when installing new software.

Installing with pip
-------------------

Alternatively, you can also use the `pip package manager
<https://pypi.org/project/pip/>`__::

    python -m pip install bordado


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from Github::

    python -m pip install https://github.com/fatiando/bordado/archive/main.zip

Alternatively, you can clone the git repository locally and install from
there::

    git clone https://github.com/fatiando/bordado.git
    cd bordado
    python -m pip install .
