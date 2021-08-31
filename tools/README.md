## PyViz Tools

This directory is used to generate a tools dashboard for comparing various Python visualization packages.

The main configuration of the dashboard is done via the ``tools.yml`` file, which can contain several sections with a list of packages, and a list of services for each section.

The dashboard is created during the website build process on Github Actions and can be seen at [pyviz.org/tools.html](http://pyviz.org/tools.html).


### Introductory text

The intro text is located in `doc/tools.md`, whose contents will be included immediately after the title on the page.

Every section can also have an `intro` in `tools.yml`. This text should also be written as markdown.

### Adding a tool

To add a tool, just create a new entry under the desired section in ``tools.yml``. At a minimum, include the GitHub org/repo for the project's source code. This will result in a project with just the badges that come from github and pypi.

** Minimal entry **

```yaml
    - repo: SciTools/cartopy
```

To include more badges, add a list of sponsors, the site that the documentation can be found at. Also feel free to add the CI information, although this information isn't currently displayed, it could easily be added later.

** More complete entry **

```yaml
    - repo: SciTools/cartopy
      sponsors: [metoffice]
      site: scitools.org.uk/cartopy
      conda_channel: conda-forge
      badges: travis, coveralls, pypi, conda
```

### Adding a sponsor

If you add a new tool that has a sponsor that is not yet found on the page, the name will not be linked and there won't be a logo. To get those assets, add an entry to ``sponsors.yml``. Use the same key as in ``tools.yml`` and include a `label` and optionally `url` and/or `logo`:

```yaml
numfocus:
  label: NumFocus
  url: https://numfocus.org
  logo: _static/badges/numfocus.png
```

If using a logo, don't forget to include a small version of the logo at `doc/_static/badges/`.
