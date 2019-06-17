# SciVis Libraries

Most of the libraries listed at PyViz.org fall into the "InfoVis" (Information Visualization) category of tools, visualizing arbitrary and potentially abstract types of information, typically in 2D or 2D+time plots with axes and numerical scales. Tools in the separate "SciVis" (Scientific Visualization) category focus on visualizing physically situated data in 3D and 3D+time, often without spatial axes and instead providing an immersive visual experience of real-world physical datasets (see [Weiskopf et al](https://pdfs.semanticscholar.org/86aa/dffeae1912a404ee66223774d6a45eefb438.pdf) for a comparison).

The SciVis tools primarily build on the 1992 OpenGL graphics standard, delivering graphics-intensive visualizations of physical processes for regular or irregularly gridded data. These libraries predate HTML5’s support for rich web applications, generally focusing on high-performance desktop-GUI applications in engineering or scientific contexts.


- The Visualization Toolkit - [VTK](https://vtk.org) (from [Kitware](https://www.kitware.com/)) supports manipulating and displaying scientific data by enabling 3D rendering, widgets for 3D interaction, and 2D plotting capability.

- [VisPy](http://vispy.org) is a high-performance interactive 2D/3D data visualization library leveraging the computational power of modern Graphics Processing Units (GPUs) through the OpenGL library to display very large datasets.

- [Glumpy](https://glumpy.github.io) is an OpenGL-based interactive visualization library in Python. Its goal is to make it easy to create fast, scalable, beautiful, interactive and dynamic visualizations.

- [GR](https://gr-framework.org) is a universal framework for cross-platform visualization applications. It offers developers a compact, portable and consistent graphics library for their programs.

- [Mayavi](https://docs.enthought.com/mayavi/mayavi) (from [Enthought](https://www.enthought.com/)) is a general purpose, cross-platform tool for 3-D scientific data visualization.

- [ParaView](https://www.paraview.org) (from [Kitware](https://www.kitware.com/)) allows users to quickly build visualizations to analyze their data using qualitative and quantitative techniques. The data exploration can be done interactively in 3D or programmatically using batch processing capabilities.

- [yt](https://yt-project.org) is a package for analyzing and visualizing volumetric data. yt supports structured, variable-resolution meshes, unstructured meshes, and discrete or sampled data such as particles.
