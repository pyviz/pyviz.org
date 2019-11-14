<img src="doc/_static/logo.png" width=150><br>

# Python tools for data visualization

|    |    |
| --- | --- |
| Build Status | [![Linux/MacOS Build Status](https://travis-ci.org/pyviz/pyviz.org.svg?branch=master)](https://travis-ci.org/pyviz/pyviz.org) |
| Website | [![gh-pages](https://img.shields.io/github/last-commit/pyviz/pyviz.org/gh-pages.svg)](https://github.com/pyviz/pyviz.org/tree/gh-pages) [![site](https://img.shields.io/website-up-down-green-red/https/pyviz.org.svg)](https://pyviz.org) |

Source material to build [pyviz.org](https://pyviz.org).  This site is owned by [NumFocus](https://numfocus.org) and is currently managed by Anaconda, Inc. for the community, but is open to everyone involved in Python data visualization; see [#2](https://github.com/pyviz/website/issues/2).

## Building pyviz.org

Whenever a PR is merged, or a commit is pushed to master, a Travis CI job is triggered that builds pyviz.org. Visit [Travis CI](https://travis-ci.org/pyviz/pyviz.org) to check on the progress of the job.

## Building dev site

To build the [dev site](https://pyviz-dev.github.io/pyviz.org), just push a commit containing the string: `website_dev`. This will start a job on Travis CI that when complete will deploy to the dev site.

**NOTE:** This will work on any branch, so it is recommended that you use it to test builds on PRs, just try not to trample on other people's toes.

## Building website locally

Set up and activate development environment:

```bash
conda env update --file environment.yml --name pyviz
conda activate pyviz
```

Build the website using the custom ``doit`` (similar to `make`) command.

```bash
doit build_website
```

**NOTE:** To build the cached badges use `doit build_cache`.

View the website locally

```bash
python -m http.server 8000
```

## Adding a tool to the "All Tools" page

See the [README](tools/README.md) in the tools directory for instructions on adding a tool to the "All Tools" page.
