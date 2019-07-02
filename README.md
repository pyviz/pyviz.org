<img src="doc/_static/logo.png" width=150><br>

# Python tools for data visualization

|    |    |
| --- | --- |
| Build Status | [![Linux/MacOS Build Status](https://travis-ci.org/pyviz/website.svg?branch=master)](https://travis-ci.org/pyviz/website) |
| Website | [![gh-pages](https://img.shields.io/github/last-commit/pyviz/website/gh-pages.svg)](https://github.com/pyviz/holoviz/tree/gh-pages) [![site](https://img.shields.io/website-up-down-green-red/http/pyviz.org.svg)](http://pyviz.org) |

Source material to build [pyviz.org](https://pyviz.org)

## Building pyviz.org

Whenever a PR is merged, or a commit is pushed to master, a Travis CI job is triggered that builds pyviz.org. Visit [Travis CI](https://travis-ci.org/pyviz/website) to check on the progress of the job.

## Building dev site

To build the [dev site](https://pyviz-dev.github.io/website), just push a commit containing the string: `website_dev`. This will start a job on Travis CI that when complete will deploy to the dev site.

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

**NOTE:** To skip badges caching, set the `--nocache` flag.

View the website locally

```bash
python -m http.server 8000
```

## Adding a tool to the "All Tools" page

See the [README](tools/README.md) in the tools directory for instructions on adding a tool to the "All Tools" page.
