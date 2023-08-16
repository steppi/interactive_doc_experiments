import matplotlib
import matplotlib.pyplot as plt
import os
import sys


import example_package

sys.path.append(os.path.abspath("./_ext"))


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'example_package'
copyright = '2023, Albert Steppi'
author = 'Albert Steppi'
release = example_package.__version__
version = example_package.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'sphinx_design',
    'matplotlib.sphinxext.plot_directive',
    'jupyterlite_sphinx',
    'sphinx_try_examples',
]

todo_include_todos = True

# Do some matplotlib config in case users have a matplotlibrc that will break
# things
matplotlib.use('agg')
plt.ioff()

templates_path = ['_templates']
exclude_patterns = []


# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

html_theme = 'pydata_sphinx_theme'

html_logo = '_static/logo.svg'
html_favicon = '_static/favicon.ico'

html_title = f"{project} v{version} Manual"
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'

html_css_files = [
    "scipy.css",
]

html_additional_pages = {}
html_use_modindex = True
html_domain_indices = False
html_copy_source = False
html_file_suffix = '.html'

htmlhelp_basename = 'scipy'

mathjax_path = "scipy-mathjax/MathJax.js?config=scipy-mathjax"
