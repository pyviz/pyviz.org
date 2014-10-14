TEMPLATE_ROW = """
  <tr>
    <td>
      {display_name}
    </td>
    <td>
      <a href="https://travis-ci.org/{user}/{package_name}">
        <img src="https://travis-ci.org/{user}/{package_name}.png?branch=master">
      </a>
    </td>
    <td>
      <a href="https://coveralls.io/r/{user}/{package_name}?branch=master">
        <img src="https://coveralls.io/repos/{user}/{package_name}/badge.png?branch=master">
      </a>
    </td>
    <td>
      <a href="https://readthedocs.org/projects/{package_name}/?badge=latest">
        <img src="https://readthedocs.org/projects/{package_name}/badge/?version=latest">
      </a>
    </td>
  </tr>
"""

TEMPLATE_TABLE = """
<html>
  <head>
    <link href='http://www.astropy.org/css/style.css' rel='stylesheet' type="text/css">
  </head>
  <body>
    <div id="wrapper">
    <h1>Astropy Project Dashboard</h1>
    <table align='center'>
      {rows}
    </table>
    </div>
  </body>
</html>
"""

PROJECTS = ['astropy/astropy', 'astrofrog/reproject', 'astrofrog/wcsaxes',
            'aplpy/aplpy', 'astropy/montage-wrapper', 'astropy/ccdproc',
            'astropy/imageutils', 'astropy/photutils', 'astropy/specutils',
            'gammapy/gammapy', 'sncosmo/sncosmo']

rows = ""

for project in PROJECTS:
    user, repo = project.split('/')
    rows += TEMPLATE_ROW.format(package_name=repo, display_name=project, user=user)

content = TEMPLATE_TABLE.format(rows=rows)

with open('status.html', 'w') as f:
    f.write(content)
