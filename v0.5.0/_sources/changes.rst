.. _changes:

Changelog
=========

Version 0.5.0
-------------

Released on: 2026/09/11

doi: https://doi.org/10.5281/zenodo.22712877

Bug fixes:

- Fix sanity check in ``rolling_window`` for the ``window_size`` parameter in higher dimensions (`#110 <https://github.com/fatiando/bordado/pull/110>`__)

New features:

- Add function ``block_split_spherical`` to split points into equal area blocks on the sphere (`#132 <https://github.com/fatiando/bordado/pull/132>`__)
- Add function ``get_spacing`` to extract spacing information from coordinates, assuming that they are from a regular grid (`#144 <https://github.com/fatiando/bordado/pull/144>`__)
- Add function ``rotate_coordinates`` to rotate coordinates in 2D space around a given point (`#128 <https://github.com/fatiando/bordado/pull/128>`__)
- Add function ``rescale_coordinates`` to translate and stretch coordinates to a new region (`#108 <https://github.com/fatiando/bordado/pull/108>`__)

Documentation

- Add a logo for Bordado (`#81 <https://github.com/fatiando/bordado/pull/81>`__)
- Add a tutorial for Bordado (`#80 <https://github.com/fatiando/bordado/pull/80>`__)
- Add a How To about calculating neighbor distances (`#158 <https://github.com/fatiando/bordado/pull/158>`__)
- Fix printing wrong variable in the line coordinates tutorial (`#157 <https://github.com/fatiando/bordado/pull/157>`__)
- Add a How To about calculating rolling averages (`#147 <https://github.com/fatiando/bordado/pull/147>`__)
- Fix docstring typos in the ``get_spacing`` function (`#145 <https://github.com/fatiando/bordado/pull/145>`__)
- Add a How To about rescaling coordinates to different region (`#143 <https://github.com/fatiando/bordado/pull/143>`__)
- Add a How To about calculating block averages on scattered data (`#142 <https://github.com/fatiando/bordado/pull/142>`__)
- Add plots to the line_coordinates tutorial to make it clearer (`#141 <https://github.com/fatiando/bordado/pull/141>`__)
- Add link to the NOAA grid registration page in our Tutorial (`#136 <https://github.com/fatiando/bordado/pull/136>`__)
- Replace NEP29 link with SPEC 0 in compatibility docs (`#114 <https://github.com/fatiando/bordado/pull/114>`__)
- Add a link to the How To page at the end of the tutorial (`#113 <https://github.com/fatiando/bordado/pull/113>`__)
- Add a 3D plot for multidimensional grids in the tutorial (`#112 <https://github.com/fatiando/bordado/pull/112>`__)
- Add a How To about selecting points inside a region (`#111 <https://github.com/fatiando/bordado/pull/111>`__)
- Add a How To about padding a region (`#105 <https://github.com/fatiando/bordado/pull/105>`__)
- Gather pages from tutorial and how to in the docs table of contents (`#103 <https://github.com/fatiando/bordado/pull/103>`__)
- Make a How To guide about getting the region of coordinates (`#98 <https://github.com/fatiando/bordado/pull/98>`__)
- Add link to the AUTHORS file in the docs navigation (`#86 <https://github.com/fatiando/bordado/pull/86>`__)
- Fix typo in Install page (`#85 <https://github.com/fatiando/bordado/pull/85>`__)
- General improvements to install and version compatibility pages (`#84 <https://github.com/fatiando/bordado/pull/84>`__)
- Add link to citation page in the README (`#82 <https://github.com/fatiando/bordado/pull/82>`__)

Maintenance:

- Add testing and support for Python 3.14 (`#89 <https://github.com/fatiando/bordado/pull/89>`__)
- Pin the version of our code linters and formatters and use Dependabot for updates (`#120 <https://github.com/fatiando/bordado/pull/120>`__, `#127 <https://github.com/fatiando/bordado/pull/127>`__, `#124 <https://github.com/fatiando/bordado/pull/124>`__, `#123 <https://github.com/fatiando/bordado/pull/123>`__, `#122 <https://github.com/fatiando/bordado/pull/122>`__, `#121 <https://github.com/fatiando/bordado/pull/121>`__)
- Revise Actions workflows to only run when necessary, saving resources and time (`#119 <https://github.com/fatiando/bordado/pull/119>`__)
- Don’t use version number pinning in Actions even for official ones, use hashes instead (`#118 <https://github.com/fatiando/bordado/pull/118>`__)
- Fix deprecation warnings in push to PyPI GitHub Action (`#117 <https://github.com/fatiando/bordado/pull/117>`__)
- Fix missing write permission in publish Actions workflow (`#116 <https://github.com/fatiando/bordado/pull/116>`__)
- Fix cache poisoning vulnerability in GitHub Actions (`#115 <https://github.com/fatiando/bordado/pull/115>`__)
- Fetch Ensaio data from GitHub when building the docs (`#106 <https://github.com/fatiando/bordado/pull/106>`__)
- Update development status to beta (ready for use but in dev) (`#102 <https://github.com/fatiando/bordado/pull/102>`__)
- Fix license specification in pyproject.toml (`#88 <https://github.com/fatiando/bordado/pull/88>`__)
- Fix broken clean target in the Makefile (`#87 <https://github.com/fatiando/bordado/pull/87>`__)
- Remove the top-level CITATION file (`#83 <https://github.com/fatiando/bordado/pull/83>`__)

This release contains contributions from:

- Sai Asish Y
- Arthur Siqueira-Macedo
- Santiago Soler
- Matt Tankersley
- Leonardo Uieda

Version 0.4.0
-------------

Released on: 2025/08/14

doi: https://doi.org/10.5281/zenodo.16874959

Bug fixes:

- Fix bug in ``spacing_to_size`` when ``start == stop``. We’d expect that the size returned would be 1 (a single point) but it was returning 2 instead because of a fix to another bug. (`#62 <https://github.com/fatiando/bordado/pull/62>`__)

New functions:

- Add function ``random_coordinates_spherical`` to generate random points on a sphere following a uniform distribution. Using the regular ``random_coordinates`` leads to larger concentration of points at the poles. (`#59 <https://github.com/fatiando/bordado/pull/59>`__)
- Add function ``rolling_window_spherical`` to generate rolling windows of roughly equal area on a sphere. It accounts for the convergence of longitude lines by increasing the longitudinal size of windows when needed and is able to wrap windows around the 360-0 longitude divide. (`#58 <https://github.com/fatiando/bordado/pull/58>`__)

Documentation:

- Fix description of step in rolling window docs (`#57 <https://github.com/fatiando/bordado/pull/57>`__)

This release contains contributions from:

- Leonardo Uieda

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
