# Dashboarding tools

Just about any Python library can be used to create a "static" PNG, SVG, HTML, or other output that can be pasted into a presentation, sent in an email, published as a figure in a paper, and so on.  Many people also want or need to create "live" Python-backed applications or dashboards that a user can interact with to explore or analyze some data. Python offers several libraries for this purpose. The four main tools designed specifically for web-based dashboarding in Python are:

- [Dash](https://plot.ly/products/dash) (from [Plotly](https://plot.ly)); see the [blog post](https://medium.com/@plotlygraphs/introducing-dash-5ecf7191b503)
- [Panel](https://panel.pyviz.org) (from [Anaconda](http://anaconda.com)); see the [blog post](https://medium.com/@philipp.jfr/panel-announcement-2107c2b15f52)
- [Voila](https://github.com/QuantStack/voila) (from [QuantStack](http://quantstack.net)); see the [blog post](https://blog.jupyter.org/and-voil%C3%A0-f6a2c08a4a93); used with separate layout tools like 
[jupyter-flex](https://github.com/danielfrg/jupyter-flex) or templates like [voila-vuetify](https://github.com/voila-dashboards/voila-vuetify).
- [Streamlit](https://www.streamlit.io); see the [blog post](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace)

You can see comparisons of these tools in:
- [Streamlit vs Dash vs Voilà vs Panel — Battle of The Python Dashboarding Giants](https://medium.datadriveninvestor.com/streamlit-vs-dash-vs-voil%C3%A0-vs-panel-battle-of-the-python-dashboarding-giants-177c40b9ea57)
  30 Mar 2021 Stephen Kilcommins. Comparing Streamlit, Dash, Voilà, and Panel for dashboarding. Links to more detailed explorations for each library individually.
- [Are Dashboards for Me?](https://towardsdatascience.com/are-dashboards-for-me-7f66502986b1)
  7 Jul 2020 Dan Lester. Overview of Python and R dashboard tools, including Voila, ipywidgets, binder, Shiny, Dash, Streamlit, Bokeh, and Panel.

There are also other tools that can be used for some aspects of dashboarding as well as many other tasks:

- [Bokeh](http://bokeh.org) is a plotting library, a widget and app library, and a server for both plots and dashboards. [Panel](https://panel.pyviz.org) is built on Bokeh, providing a higher-level toolkit specifically focused on app and dashboard creation and supporting multiple plotting libraries (not just Bokeh).

- [ipywidgets](https://ipywidgets.readthedocs.io) provides a wide array of Jupyter-compatible widgets and an interface supported by many Python libraries, but sharing as a dashboard requires a separate deployable server like [Voila](https://github.com/QuantStack/voila).

- [matplotlib](http://matplotlib.org) supports many different backends, including several native GUI toolkit interfaces such as Qt that can be used for building arbitrarily complex native applications that can be used instead of a web-based dashboard like those above.

- [Bowtie](https://github.com/jwkvam/bowtie) (from Jacques Kvam) allows users to build dashboards in pure Python.

- [flask](http://flask.pocoo.org/) is a Python-backed web server that can be used to build arbitrary web sites, including those with Python plots that then function as [flask dashboards](https://pusher.com/tutorials/live-dashboard-python), but is not specifically set up to make dashboarding easier.
