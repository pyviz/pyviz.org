# SciVis Libraries

Most of the libraries listed at PyViz.org fall into the [InfoVis](http://ieeevis.org/year/2019/info/call-participation/infovis-paper-types) (Information Visualization) category of tools, visualizing arbitrary and potentially abstract types of information, typically in 2D or 2D+time plots with axes and numerical scales. Tools in the separate [SciVis](http://ieeevis.org/year/2019/info/call-participation/scivis-paper-types) (Scientific Visualization) category focus on visualizing physically situated gridded data in 3D and 3D+time, often without spatial axes and instead providing an immersive visual experience of real-world physical datasets (see [Weiskopf et al](https://pdfs.semanticscholar.org/86aa/dffeae1912a404ee66223774d6a45eefb438.pdf) for a comparison). Desktop-GUI targeted SciVis tools build on the OpenGL graphics standard, while browser-based web applications usually leverage the related WebGL graphics standard.

SciVis libraries supporting Python:

- The Visualization Toolkit - [VTK](https://vtk.org) (from [Kitware](https://www.kitware.com/)) supports manipulating and displaying scientific data by enabling 3D rendering, widgets for 3D interaction, and 2D plotting capability.

- [VisPy](http://vispy.org) is a high-performance interactive 2D/3D data visualization library leveraging the computational power of modern Graphics Processing Units (GPUs) through the OpenGL library to display very large datasets.

- [Glumpy](https://glumpy.github.io) is an OpenGL-based interactive visualization library in Python. Its goal is to make it easy to create fast, scalable, beautiful, interactive and dynamic visualizations.

- [GR](https://gr-framework.org) is a universal framework for cross-platform visualization applications. It offers developers a compact, portable and consistent graphics library for their programs.

- [Mayavi](https://docs.enthought.com/mayavi/mayavi) (from [Enthought](https://www.enthought.com/)) is a general purpose, cross-platform tool for 3-D scientific data visualization.

- [ParaView](https://www.paraview.org) (from [Kitware](https://www.kitware.com/)) is an application built on the Visualization Toolkit (VTK) with extensions for distributed computing. ParaView allows users to quickly build visualizations to analyze their data using qualitative and quantitative techniques. The data exploration can be done interactively in 3D or programmatically using batch processing capabilities.

- [yt](https://yt-project.org) is a package for analyzing and visualizing volumetric data. yt supports structured, variable-resolution meshes, unstructured meshes, and discrete or sampled data such as particles.

- [PyVista](http://www.pyvista.org) is a streamlined interface for the Visualization Toolkit (VTK) providing 3D plotting and mesh analysis with NumPy support being at its core. PyVista supports point clouds, structured/unstructured meshes, and volumetric datasets.

- [vedo](https://vedo.embl.es) is a lightweight module for scientific analysis and visualization of polygonal meshes, point clouds and volumetric data. It offers an intuitive API which can be combined with VTK seamlessly in a program, whilst mantaining access to the full range of VTK native classes.

- [itk-jupyter-widgets](https://github.com/InsightSoftwareConsortium/itk-jupyter-widgets), based on the Visualization Toolkit for JavaScript [vtk.js](https://kitware.github.io/vtk-js/index.html) and the [Insight Toolkit (ITK)](https://www.itk.org/), provides interactive 3D widgets for Jupyter to visualize and analyze images, point sets, and meshes.
