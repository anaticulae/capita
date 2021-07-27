# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Table Detector
=======================
"""

import re

import serializeraw
import utila

import sections.table.strategy


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages: tuple = None,
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
        headline=HEADLINES_TABLETABLE,
        noheadlines=NOHEADLINES_TABLETABLE,
        pattern=table,
        shortcut='tableoftable',
        topsearch=False,
    )
    return dumped


HEADLINES_TABLETABLE = utila.splitlines("""
LIST OF TABLES
TABELLEN
TABELLENVERZEICHNIS
""")

NOHEADLINES_TABLETABLE = utila.splitlines("""
ABBILDUNGEN
ABBILDUNGSVERZEICHNIS
INHALT
INHALTSVERZEICHNIS
""")

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
    return False
