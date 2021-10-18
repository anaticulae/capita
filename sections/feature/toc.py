# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Toc Likelihood Detector
=======================

TODO:
    - support table of figures
              table of abbreviation
"""

import re

import serializeraw
import utila

import sections.table.strategy

# no possible toc later than page 20
VALID_TOC_PAGES = utila.ranged_tuple(0, 20)  # HOLY VALUE

HEADLINES = utila.splitlines("""
Contents
Inhalt
Inhaltsverzeichnis
Table of Content
Table of Contents
""")

NOHEADLINES = utila.splitlines("""
Abbildungen
Abbildungsverzeichnis
Tabellen
Tabellenverzeichnis
""")


def work(
    oneline_text: str,
    oneline_textposition: str,
    sizeandborder: str,
    headerfooters: str,
    pages=None,
) -> str:
    # TODO: SHRINK PAGES BY VALID_TOC_PAGES?
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=oneline_text,
        textpositions=oneline_textposition,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    dumped = sections.table.strategy.work(
        ptcns,
        headline=HEADLINES,
        noheadlines=NOHEADLINES,
        shortcut='toc',
        pages=VALID_TOC_PAGES,
        second=True,
        pattern=appendix_line,
    )
    return dumped


APPENDIX = re.compile(
    r'(ANHANG|APPENDIX)[ ]{0,3}\d{1,2}[ ]{0,3}:{0,1}[ ]{0,5}.{0,50}\d{1,3}',
    re.X,
)


def appendix_line(line: str) -> bool:
    """\
    >>> appendix_line('ANHANG 4: ABBILDUNGSVERZEICHNIS               251')
    True
    """
    if APPENDIX.match(line):
        return True
    return False
