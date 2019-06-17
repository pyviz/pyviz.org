# SciVis Libraries

SciVis tools cover important functionality not addressed by InfoVis-focused libraries, offering advanced and specialized visualization techniques for large and complex finite-element-method simulations. By focussing on visualizing physically situated data in desktop applications these tools support visualization of a variety of data structures and the “long tail” of scientific research beyond just the initial visualization itself.

These tools primarily build on the 1992 OpenGL graphics standard, delivering graphics-intensive visualizations of physical processes in three or four dimensions (3D over time), for regular or irregularly gridded data. These libraries predate HTML5’s support for rich web applications, generally focusing on high-performance desktop-GUI applications in engineering or scientific contexts.

Can generally handle very large gridded datasets (gigabytes or larger) using compiled data libraries and native GUI apps.

- The Visualization Toolkit - [VTK](https://vtk.org) (from [Kitware](https://www.kitware.com/)) supports manipulating and displaying scientific data by enabling 3D rendering, widgets for 3D interaction, and 2D plotting capability.

- [VisPy](http://vispy.org) is a high-performance interactive 2D/3D data visualization library leveraging the computational power of modern Graphics Processing Units (GPUs) through the OpenGL library to display very large datasets.

- [Glumpy](https://glumpy.github.io) is an OpenGL-based interactive visualization library in Python. Its goal is to make it easy to create fast, scalable, beautiful, interactive and dynamic visualizations.

- [GR](https://gr-framework.org) is a universal framework for cross-platform visualization applications. It offers developers a compact, portable and consistent graphics library for their programs.

- [Mayavi](https://docs.enthought.com/mayavi/mayavi) (from [Enthought](https://www.enthought.com/)) is a general purpose, cross-platform tool for 3-D scientific data visualization.

- [ParaView](https://www.paraview.org) (from [Kitware](https://www.kitware.com/)) allows users to quickly build visualizations to analyze their data using qualitative and quantitative techniques. The data exploration can be done interactively in 3D or programmatically using batch processing capabilities.

- [yt](https://yt-project.org) is a package for analyzing and visualizing volumetric data. yt supports structured, variable-resolution meshes, unstructured meshes, and discrete or sampled data such as particles.