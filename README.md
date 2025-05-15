<h1 align="center">Bordado</h1>

<p align="center"><strong>Create, manipulate, and split geographic coordinates</strong></p>

<p align="center">
<a href="https://www.fatiando.org/bordado"><strong>Documentation</strong> (latest)</a> •
<a href="https://www.fatiando.org/bordado/dev"><strong>Documentation</strong> (main branch)</a> •
<a href="https://github.com/fatiando/bordado/blob/main/CONTRIBUTING.md"><strong>Contributing</strong></a> •
<a href="https://www.fatiando.org/contact/"><strong>Contact</strong></a> •
<a href="https://github.com/orgs/fatiando/discussions"><strong>Ask a question</strong></a>
</p>

<p align="center">
Part of the
<a href="https://www.fatiando.org"><strong>Fatiando a Terra</strong></a>
project.
</p>

<p align="center">
<a href="https://pypi.python.org/pypi/bordado"><img src="http://img.shields.io/pypi/v/bordado.svg?style=flat-square" alt="Latest version on PyPI"></a>
<a href="https://github.com/conda-forge/bordado-feedstock"><img src="https://img.shields.io/conda/vn/conda-forge/bordado.svg?style=flat-square" alt="Latest version on conda-forge"></a>
<a href="https://pypi.python.org/pypi/bordado"><img src="https://img.shields.io/pypi/pyversions/bordado.svg?style=flat-square" alt="Compatible Python versions."></a>
<a href="https://doi.org/10.5281/zenodo.15051755"><img src="https://img.shields.io/badge/doi-10.5281%2Fzenodo.15051755-blue?style=flat-square" alt="DOI used to cite bordado"></a>
</p>

## About

**Bordado**  (Portuguese for "embroidery") is a Python package for creating,
manipulating, and splitting geographic and Cartesian coordinates.
It can generate coordinates at regular intervals by specifying the number of
points or the spacing between points. Bordado takes care of adjusting the
spacing to make sure it matches the specified domain/region. It also contains
functions for splitting coordinates into spatial blocks and more.

> Many of these functions used to be in
> [Verde](https://www.fatiando.org/verde/) but were moved to Bordado to make
> them more accessible without all of the extra dependencies that Verde
> requires.

## Project goals

* Generate regular point distributions in grids, profiles, lines, etc.
* Provide functions for fast spatial blocking and coordinates manipulation.
* Have minimal dependencies to make it easy to install and light to pick up for
  other projects.

## Project status

**Bordado is in early stages of development** but is already functional. We
only caution that we may still make changes to the API so things may break
between releases.

**We welcome feedback and ideas!** This is a great time to bring new ideas on
how we can improve the project.
[Join the conversation](https://www.fatiando.org/contact) or submit
[issues on GitHub](https://github.com/fatiando/bordado/issues).

## Getting involved

🗨️ **Contact us:**
Find out more about how to reach us at
[fatiando.org/contact](https://www.fatiando.org/contact/).

👩🏾‍💻 **Contributing to project development:**
Please read our
[Contributing Guide](https://github.com/fatiando/bordado/blob/main/CONTRIBUTING.md)
to see how you can help and give feedback.

🧑🏾‍🤝‍🧑🏼 **Code of conduct:**
This project is released with a
[Code of Conduct](https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

> **Imposter syndrome disclaimer:**
> We want your help. **No, really.** There may be a little voice inside your
> head that is telling you that you're not ready, that you aren't skilled
> enough to contribute. We assure you that the little voice in your head is
> wrong. Most importantly, **there are many valuable ways to contribute besides
> writing code**.
>
> *This disclaimer was adapted from the*
> [MetPy project](https://github.com/Unidata/MetPy).

## License

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
[`LICENSE.txt`](https://github.com/fatiando/bordado/blob/main/LICENSE.txt).
