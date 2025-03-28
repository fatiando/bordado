.. _changes:

Changelog
=========

Version 0.1.0
-------------

Released on: 2025/03/28

doi: https://doi.org/10.5281/zenodo.15102594

The functions below are originally from the `Verde <https://www.fatiando.org/verde/>`__ library and have been moved here and improved upon:

- Add function ``rolling_window`` to split points into rolling windows (`#31 <https://github.com/fatiando/bordado/pull/31>`__)
- Add function ``block_split`` to split points into blocks (`#30 <https://github.com/fatiando/bordado/pull/30>`__)
- Add function ``grid_coordinates`` to generate n-dimensional grids with evenly spaced points (`#18 <https://github.com/fatiando/bordado/pull/18>`__)
- Add function ``random_coordinates`` to make a random scatter of points in n-dimensions (`#25 <https://github.com/fatiando/bordado/pull/25>`__ and `#26 <https://github.com/fatiando/bordado/pull/26>`__)
- Add function ``inside`` to check which points are in a region (`#24 <https://github.com/fatiando/bordado/pull/24>`__)
- Add function ``get_region`` to get the bounding box of the given set of coordinates (`#16 <https://github.com/fatiando/bordado/pull/16>`__)
- Add function ``pad_region`` to expand a region by a specified amount (`#15 <https://github.com/fatiando/bordado/pull/15>`__)
- Add function ``line_coordinates`` to generate 1D evenly-spaced coordinates (`#13 <https://github.com/fatiando/bordado/pull/13>`__)

Improvements over their Verde counterparts:

- All functions now work with more than 2 dimensions.
- Argument names have been changed to make them more reasonable, for example ``spacing`` in ``block_split`` was renamed to ``block_size``.
- Functions perform more sanity checks on their arguments to avoid common mistakes.
- When adjusting a region because the spacing is not a multiple of it, change both the lower and the upper boundaries to spread the change more evenly (`#21 <https://github.com/fatiando/bordado/pull/21>`__)
- Optional arguments to functions are now keyword-only, avoiding the common mistake of passing a spacing in the place of a shape when not using keywords (`#20 <https://github.com/fatiando/bordado/pull/20>`__)

Bordado also exposes some sanity checks that other packages can use:

- Add function ``check_coordinates`` to check that all coordinates have same shape and make sure they are arrays (`#29 <https://github.com/fatiando/bordado/pull/29>`__)
- Add function ``check_region`` to make sure the region has an even number of arguments and they are in the right order (`#12 <https://github.com/fatiando/bordado/pull/12>`__ and `#14 <https://github.com/fatiando/bordado/pull/14>`__)

This release contains contributions from:

- Leonardo Uieda

Version 0.0.1
-------------

Released on: 2025/03/19

doi: https://doi.org/10.5281/zenodo.15051756

This is the first release of Bordado, used to guarantee the package name and
setup the development infrastructure. The next release will contain actual code
for users.

This release contains contributions from:

- Leonardo Uieda
