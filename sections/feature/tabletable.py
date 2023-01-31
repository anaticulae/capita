# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Table Detector
=======================
"""

import re

import elements.headline.lookup
import serializeraw

import sections.strategy
import sections.table


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages: tuple = None,
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
        headline=elements.headline.lookup.TABLETABLE,
        noheadlines=NOHEADLINES,
        pattern=table,
        shortcut='tableoftable',
        topsearch=False,
    )
    return dumped


NOHEADLINES = (elements.headline.lookup.TOC |
               elements.headline.lookup.FIGURETABLE |
               elements.headline.lookup.LISTINGS)

TABLE = re.compile(
    r'(Tab\.{0,1}|Tabelle)[ ]{0,3}\d{1,2}[ ]{0,3}.{0,50}',
    re.X | re.I,
)
TABLE_ENG = re.compile(
    r'TABLE[ ]{0,3}\d{1,2}\-\d{1,2}\.[ ]{0,3}.{0,50}',
    re.X | re.I,
)


def table(line: str) -> bool:
    """\
    >>> table('Tabelle 4 - Aufgabenüberblick der Reflexionsphase ................... 65')
    True
    >>> table('TABLE 3-1. Evaluation of Hypermedia                         41')
    True
    """
    if TABLE.match(line):
        return True
    if TABLE_ENG.match(line):
        return True
    if sections.table.valid_line(line):
        return True
    return False
