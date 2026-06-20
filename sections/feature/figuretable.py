# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Figure Detector
========================
"""

import re

import elementae.headline.lookup
import serializeraw
import utilo

import sections.strategy
import sections.table

NOHEADLINES = utilo.a_minus_b(  #pylint:disable=no-member
    elementae.headline.lookup.HEADLINES,
    elementae.headline.lookup.FIGURETABLE,
)


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages=None,
) -> str:
    ptcns = serializeraw.ptcn_fromfile(
        text=text_linewise,
        textpositions=textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooters,
        pages=pages,
    )
    dumped = sections.strategy.work(
        ptcns,
        headline=elementae.headline.lookup.FIGURETABLE,
        noheadlines=NOHEADLINES,
        shortcut='figuretable',
        pattern=figure,
    )
    return dumped


FIGURE = re.compile(
    r'(Abb\.{0,1}|Abbildung)[ ]{0,3}\d{1,2}[ ]{0,3}.{0,50}',
    re.X | re.I,
)
FIGURE_ENG = utilo.compiles(r"""
    FIGURE[ ]{0,3}
    \d{1,2}(\-\d{1,2}\.)?
    [ ]{0,3}
    .{0,50}
""")


def figure(line: str) -> bool:
    """\
    >>> figure('Abb. 7        Durchschnittliche Reaktionszeit (korrekte und')
    True
    >>> figure('Figure 5-5. Early WWW Architecture Diagram              81')
    True
    >>> figure('Figure 13   Architecture of a VAE. . . . . . . . . . . . . . . . 43 ')
    True
    """
    if FIGURE.match(line):
        return True
    if FIGURE_ENG.match(line):
        return True
    if sections.table.valid_line(line):
        return True
    return False
