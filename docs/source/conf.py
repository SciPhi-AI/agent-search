# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from docutils import nodes
from docutils.parsers.rst import roles

# -- Project information -----------------------------------------------------

project = "AgentSearch"
copyright = "2023, Emergent AGI Inc."
author = "the AgentSearch Team"


def white_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.inline(rawtext, text, classes=["white"])
    return [node], []


def setup(app):
    roles.register_local_role("white", white_role)


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    # "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    # "sphinx_rtd_dark_mode"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# Exclude the prompt "$" when copying code
copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_title = project
html_theme = "sphinx_book_theme"
html_logo = "assets/logos/sciphi.png"
html_theme_options = {
    "logo_only": True,
    "path_to_docs": "docs/source",
    "repository_url": "https://github.com/SciPhi-AI/agent-search",
    "use_repository_button": True,
}

# user starts in dark mode
default_dark_mode = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
