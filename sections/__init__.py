#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Sections
========

The `sections` tool is a very lightwight tool to determine the
likelihood of a feature on a page very quickly. Sections is runned to
determine which feature extraction should runned on which pages.

Plan
----

The result of the section tool is a plan for the feature extractor.
Further plans for judgements and informations for the user are not
provided by sections tool. The section tool extracts only features but
do not judges the result.

Sources
-------

Data Provider:

* Rawmaker
* Linero
* Imagero (planned)
* Figero (planned)
* Tabelero (planned)


Feature Provider:

* Groupme
* Detector

Planned Features
----------------

The following sections are planned to be supported:

.. code-block:: none

  * Introduction
      * Titlepage
      * Thank you
      * Copyright etc.
      * Erklaerung
  * Table-Area
      * Table of content
      * Short cuts
      * Figure table
  * Content
      * Chapter
          * Figure
          * Text
          * Headlines
  * Table-Area-B
  * Appendix
      * Resources
      * Link
      * Bibliography
"""

import os

import sections.__patch__
import sections.path

__version__ = '1.20.0'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROCESS = 'sections'
PACKAGE = 'sections'
