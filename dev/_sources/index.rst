.. title:: Home


.. raw:: html

   <h1 class="display-1">Bordado</h1>

.. div:: sd-fs-3

   Create, manipulate, and split geographic coordinates


**Bordado**  (Portuguese for "embroidery") is a Python package for creating,
manipulating, and splitting geographic and Cartesian coordinates.
It can generate coordinates at regular intervals by specifying the number of
points or the spacing between points. Bordado takes care of adjusting the
spacing to make sure it matches the specified domain/region. It also contains
functions for splitting coordinates into spatial blocks and more.

.. seealso::

   Many of the functions here used to be in
   `Verde <https://www.fatiando.org/verde/>`__. They were moved to Bordado to
   make them more accessible without all of the extra dependencies that Verde
   requires. We have also improved and expanded most of the functions ported
   from Verde.

.. grid:: 1 2 1 2
    :margin: 5 5 0 0
    :padding: 0 0 0 0
    :gutter: 4

    .. grid-item-card:: :octicon:`rocket` Getting started
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        New to Bordado? Start here!

        .. button-ref:: overview
            :click-parent:
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`comment-discussion` Need help?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Ask on our community channels

        .. button-link:: https://www.fatiando.org/contact
            :click-parent:
            :color: primary
            :outline:
            :expand:

             Join the conversation

    .. grid-item-card:: :octicon:`file-badge` Reference documentation
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        A list of modules and functions

        .. button-ref:: api
            :click-parent:
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`bookmark` Using Bordado for research?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Citations help support our work

        .. button-ref:: citing
            :click-parent:
            :color: primary
            :outline:
            :expand:

.. seealso::

    Bordado is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.

.. toctree::
    :hidden:
    :maxdepth: 1
    :caption: Getting Started

    overview.rst
    install.rst

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    citing.rst
    changes.rst
    compatibility.rst
    versions.rst


.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Community

    Join the community <http://contact.fatiando.org>
    How to contribute <https://github.com/fatiando/bordado/blob/main/CONTRIBUTING.md>
    Code of Conduct <https://github.com/fatiando/bordado/blob/main/CODE_OF_CONDUCT.md>
    Source code on GitHub <https://github.com/fatiando/bordado>
    The Fatiando a Terra project <https://www.fatiando.org>
