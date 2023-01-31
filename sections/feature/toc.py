# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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

import configo
import elements.headline.lookup
import serializeraw
import utila

import sections.strategy
import sections.table

# no possible toc later than page 20

VALID_TOC_PAGES_MIN = configo.HV_INT_PLUS(default=0)

VALID_TOC_PAGES_MAX = configo.HV_INT_PLUS(default=20)


def work(
    oneline_text: str,
    oneline_textposition: str,
    sizeandborder: str,
    headerfooters: str,
    pages=None,
) -> str:
    pages = pages_inside(
        pages,
        minn=VALID_TOC_PAGES_MIN,
        maxx=VALID_TOC_PAGES_MAX,
    )
    ptcns = serializeraw.ptcn_fromfile(
        text=oneline_text,
        textpositions=oneline_textposition,
        sizeandborder=sizeandborder,
        headerfooter=headerfooters,
        pages=pages,
    )
    dumped = sections.strategy.work(
        ptcns,
        headline=elements.headline.lookup.TOC,
        noheadlines=NOHEADLINES,
        shortcut='toc',
        second=True,
        pattern=appendix_line,
    )
    return dumped


NOHEADLINES = (elements.headline.lookup.TABLETABLE |
               elements.headline.lookup.FIGURETABLE |
               elements.headline.lookup.LISTINGS)

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
    if sections.table.valid_line(line):
        return True
    return False


def pages_inside(pages: tuple, minn: int = 0, maxx=None) -> tuple:
    """\
    >>> pages_inside(None, 5, 10)
    (5, 6, 7, 8, 9, 10)
    >>> pages_inside((0, 1, 2, 3, 4, 5), 2, maxx=4)
    (2, 3, 4)
    """
    # TODO: MOVE TO UTILA
    if not pages:
        if maxx is None:
            return None
        return utila.rtuple(minn, maxx + 1)
    pages = tuple(item for item in pages if minn <= item <= maxx)
    return pages
