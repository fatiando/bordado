.. title:: Home

.. grid::
    :gutter: 2 3 3 3
    :margin: 5 5 0 0
    :padding: 0 0 0 0

    .. grid-item::
        :columns: 12 8 8 8

        .. raw:: html

            <h1 class="display-1">Bordado</h1>

        .. div:: sd-fs-3

            Create, manipulate, and split geographic coordinates

    .. grid-item::
        :columns: 12 4 4 4

        .. image:: ./_static/bordado-logo.svg
            :width: 200px
            :class: sd-m-auto dark-light

**Bordado** (Portuguese for "embroidery") is a Python package for creating,
manipulating, and splitting geographic and Cartesian coordinates.
It can generate coordinates at regular intervals by specifying the number of
points or the spacing between points. Bordado takes care of adjusting the
spacing to make sure it matches the specified domain/region. It also contains
functions for splitting coordinates into spatial blocks and more.

.. seealso::

    Bordado is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.

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

.. admonition:: Look familiar?
    :class: seealso

    Many of the functions here used to be in
    `Verde <https://www.fatiando.org/verde/>`__. They were moved to Bordado to
    make them more accessible without all the extra dependencies that Verde
    requires. We have also improved and expanded most of the functions ported
    from Verde.

----

Project status
--------------

**Bordado is ready for use but still changing**. This means that we are
still adding a lot of new features, and sometimes we make changes to the
ones we already have while we try to improve the software based on
users’ experience, test new ideas, take better design decisions, etc.
Some of these changes could be **backwards incompatible**. Keep that in
mind before you update Harmonica to a newer version.

**We welcome feedback and ideas!** This is a great time to bring new
ideas on how we can improve the project. `Join the
conversation <https://www.fatiando.org/contact>`__ or submit `issues on
GitHub <https://github.com/fatiando/bordado/issues>`__.

Getting involved
----------------

🗨️ **Contact us:** Find out more about how to reach us at
`fatiando.org/contact <https://www.fatiando.org/contact/>`__.

👩🏾‍💻 **Contributing to project development:** Please read our
`Contributing
Guide <https://github.com/fatiando/bordado/blob/main/CONTRIBUTING.md>`__
to see how you can help and give feedback.

🧑🏾‍🤝‍🧑🏼 **Code of conduct:** This project is released with a `Code of
Conduct <https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

    **Imposter syndrome disclaimer:** We want your help. **No, really.** There
    may be a little voice inside your head that is telling you that you’re
    not ready, that you aren’t skilled enough to contribute. We assure you
    that the little voice in your head is wrong. Most importantly, **there are
    many valuable ways to contribute besides writing code** (giving feedback,
    teaching, writing documentation, and more).

    *This disclaimer was adapted from the* `MetPy
    project <https://github.com/Unidata/MetPy>`__.

License
-------

This is free software: you can redistribute it and/or modify it under
the terms of the **BSD 3-clause License**. A copy of this license is
provided in the
`LICENSE.txt <https://github.com/fatiando/bordado/blob/main/LICENSE.txt>`__
file.


.. toctree::
    :hidden:
    :maxdepth: 1
    :caption: Getting Started

    overview.rst
    install.rst

.. toctree::
    :hidden:
    :maxdepth: 1
    :caption: User Guide

    tutorial/index.rst
    how-to/index.rst

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    citing.rst
    references.rst
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
    Authors <https://github.com/fatiando/bordado/blob/main/AUTHORS.md>
    The Fatiando a Terra project <https://www.fatiando.org>
