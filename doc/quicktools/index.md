# Quick viz tools

The full list of [Python viz tools](../tools) is very long and covers a wide range of functionality. Many users share similar needs, and can get very far using a high-level tool that covers the most common tasks succinctly and conveniently, typically by providing a simpler API on top of an existing plotting tool.


## Pandas .plot() API

The longest-established of these tools is the [Pandas .plot() API](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html). This basic plotting interface uses [Matplotlib](http://matplotlib.org) to render static PNGs in a Jupyter notebook or for exporting from Python, with a command that can be as simple as `df.plot()` for a DataFrame with two columns.

The Pandas .plot() API has emerged as a de-facto standard for high-level plotting APIs in Python, and is now supported by many different libraries that use other underlying plotting engines to provide additional power and flexibility. Thus learning this API allows you to access capabilities provided by a wide variety of underlying tools, with relatively little additional effort. The libraries currently supporting this API include:

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html) -- Matplotlib-based API included with Pandas. Static PNG output in Jupyter notebooks.
- [PdVega](https://altair-viz.github.io/pdvega) -- Vega-lite-based, JSON-encoded interactive plots.
- [hvPlot](https://hvplot.pyviz.org) -- HoloViews and Bokeh-based interactive plots for Pandas, GeoPandas, Xarray, Dask, Intake, and Streamz data.
- [Pandas Bokeh](https://github.com/PatrikHlobil/Pandas-Bokeh) -- Bokeh-based interactive plots, for Pandas, GeoPandas, and Pyspark data.
- [Cufflinks](https://github.com/santosjorge/cufflinks) -- Plotly-based interactive plots for Pandas data.

## Other high-level APIs

- [Chartify](https://github.com/spotify/chartify) -- Bokeh-based interactive plots for tidy data.
- [HoloViews](https://holoviews.org) -- Bokeh, Matplotlib, or Plotly-based interactive plots for tidy data.
- [Plotly Express](https://www.plotly.express/) -- Plotly-based interactive plots.
- [Altair](https://altair-viz.github.io/) -- Vega-lite-based interactive plots.
