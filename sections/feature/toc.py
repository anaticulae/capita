# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import serializeraw
import utila

import sections.table.strategy

# no possible toc later than page 20
VALID_TOC_PAGES = utila.ranged_tuple(0, 20)  # HOLY VALUE

HEADLINES = [
    'Inhalt',
    'Inhaltsverzeichnis',
    'Contents',
]

NOHEADLINES = [
    'Abbildungen',
    'Abbildungsverzeichnis',
    'Tabellen',
    'Tabellenverzeichnis',
]


def work(
        oneline_text: str,
        oneline_textposition: str,
        sizeandborder: str,
        headerfooters: str,
        pages=None,
) -> str:
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
    )
    return dumped
