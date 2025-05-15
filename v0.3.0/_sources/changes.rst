.. _changes:

Changelog
=========

Version 0.3.0
-------------

Released on: 2025/05/15

doi: https://doi.org/10.5281/zenodo.15427887

**Breaking changes:**

- Remove validation functions ``check_coordinates``, ``check_region``, and ``check_shape`` from the public API because they will tend to be specific to individual projects, causing compatibility problems for us when our requirements change (`#49 <https://github.com/fatiando/bordado/pull/49>`__)

New functions:

- Add function ``great_circle_coordinates`` to make points at regular distances along a great circle on a sphere (`#50 <https://github.com/fatiando/bordado/pull/50>`__)
- Add and expand to n-dimenions the function ``profile_coordinates`` from Verde to generate evenly spaced points between two reference points points (`#48 <https://github.com/fatiando/bordado/pull/48>`__)
- Add function ``neighbor_distance_statistics`` to calculate statistics of the distances to nearest neighbors of points. This is a generalization of the function ``median_distance`` from Verde (`#46 <https://github.com/fatiando/bordado/pull/46>`__)
- Add and expand function ``shape_to_spacing`` from Verde to convert a shape (numbers of points) to spacings (`#44 <https://github.com/fatiando/bordado/pull/44>`__)
- Make function ``spacing_to_size`` public in the API instead of private (`#43 <https://github.com/fatiando/bordado/pull/43>`__)

Improvements:

- Add check for invalid size argument in ``line_coordinates`` (`#47 <https://github.com/fatiando/bordado/pull/47>`__)

Documentation:

- Add an Overview page to the documentation that covers basic functionality and explains a bit about what the package does (`#51 <https://github.com/fatiando/bordado/pull/51>`__)

Maintenance:

- Specify coverage source in ``pyproject.toml`` (`#42 <https://github.com/fatiando/bordado/pull/42>`__)

This release contains contributions from:

- Leonardo Uieda

Version 0.2.0
-------------

Released on: 2025/05/08

doi: https://doi.org/10.5281/zenodo.15360679

**Breaking changes:**

- Rename the ``rng`` argument of ``bordado.random_coordinates`` to ``random_seed``, which is more explicit and won’t be confused with “range” (`#34 <https://github.com/fatiando/bordado/pull/34>`__)

New functions ported from `Verde <https://www.fatiando.org/verde>`__ and improved:

- New function ``bordado.expanding_window`` to split points with n dimensions on windows that share a common center but expand in size (`#37 <https://github.com/fatiando/bordado/pull/37>`__)

Enhancements:

- Make sure ``bordado.get_region`` works with pandas and xarray inputs (`#36 <https://github.com/fatiando/bordado/pull/36>`__)

Maintenance:

- Pin third-party Actions using commit hashes instead of tags for security (`#39 <https://github.com/fatiando/bordado/pull/39>`__)

This release contains contributions from:

- Santiago Soler
- Leonardo Uieda

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
