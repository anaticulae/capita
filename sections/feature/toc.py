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

import utila

import sections.table.strategy

# no possible toc later than page 20
VALID_TOC_PAGES = utila.ranged_tuple(0, 20)  # HOLY VALUE

HEADLINES = [
    'Inhalt',
    'Inhaltsverzeichnis',
    'Contents',
]

BLACKLIST = [
    'Abbildungen',
    'Abbildungsverzeichnis',
    'Tabellen',
    'Tabellenverzeichnis',
]


def work(text_linewise: str, textpositions: str, pages=None) -> str:
    dumped = sections.table.strategy.work(
        text_linewise,
        textpositions,
        headline=HEADLINES,
        blacklist=BLACKLIST,
        shortcut='toc',
        valid_pages=VALID_TOC_PAGES,
        pages=pages,
    )
    return dumped
