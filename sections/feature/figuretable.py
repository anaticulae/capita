# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Figure Detector
========================
"""

import re

import elements.headline.lookup
import serializeraw

import sections.table.strategy

NOHEADLINES = elements.headline.lookup.HEADLINES - elements.headline.lookup.FIGURETABLE


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages=None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text_linewise,
        textpositions=textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    dumped = sections.table.strategy.work(
        ptcns,
        headline=elements.headline.lookup.FIGURETABLE,
        noheadlines=NOHEADLINES,
        shortcut='figuretable',
        pattern=figure,
    )
    return dumped


FIGURE = re.compile(
    r'(Abb\.{0,1}|Abbildung)[ ]{0,3}\d{1,2}[ ]{0,3}.{0,50}',
    re.X | re.I,
)
FIGURE_ENG = re.compile(
    r'FIGURE[ ]{0,3}\d{1,2}\-\d{1,2}\.[ ]{0,3}.{0,50}',
    re.X | re.I,
)


def figure(line: str) -> bool:
    """\
    >>> figure('Abb. 7        Durchschnittliche Reaktionszeit (korrekte und')
    True
    >>> figure('Figure 5-5. Early WWW Architecture Diagram              81')
    True
    """
    if FIGURE.match(line):
        return True
    if FIGURE_ENG.match(line):
        return True
    return False
