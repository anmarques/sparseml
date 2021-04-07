# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "SparseML"
copyright = (
    "2021 - present / Neuralmagic, Inc. All Rights Reserved. "
    'Licensed under the Apache License, Version 2.0 (the "License")'
)
author = "Neural Magic"

# The full version, including alpha/beta/rc tags
version = "unknown"
version_major_minor = version
# load and overwrite version info from sparseml package
exec(open(os.path.join(os.pardir, "src", "sparseml", "version.py")).read())
release = version
version = version_major_minor
print(f"loaded versions from src/sparseml/version.py and set to {release}, {version}")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_markdown_tables",
    "sphinx_multiversion",
    "sphinx_rtd_theme",
    "recommonmark",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Whitelist pattern for tags (set to None to ignore all tags)
smv_tag_whitelist = r'^v.*$'

# Whitelist pattern for branches (set to None to ignore all branches)
smv_branch_whitelist = r'^main$'

# Whitelist pattern for remotes (set to None to use local branches only)
smv_remote_whitelist = r'^.*$'

# Pattern for released versions
smv_released_pattern = r'^tags/v.*$'

# Format for versioned output directories inside the build directory
smv_outputdir_format = '{ref.name}'

# Determines whether remote or local git branches/tags are preferred if their output dirs conflict
smv_prefer_remote_refs = False

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]
# source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "source/icon-sparseml.png"

html_theme_options = {
    'analytics_id': 'UA-128364174-1',  #  Provided by Google in your dashboard
    'analytics_anonymize_ip': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = ["css/nm-theme-adjustment.css"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

html_favicon = "favicon.ico"

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "sparsemldoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # "papersize": "letterpaper",
    # "pointsize": "10pt",
    # "preamble": "",
    # "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "sparseml.tex", "SparseML Documentation", [author], "manual",),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "sparseml", "SparseML Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "sparseml",
        "SparseML Documentation",
        author,
        "sparseml",
        (
            "Libraries for state-of-the-art deep neural network optimization "
            "algorithms, enabling simple pipelines integration with a few lines of code"
        ),
        "Miscellaneous",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = []


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------
