# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table of Figure Detector
========================
"""

import serializeraw

import sections.table.strategy


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
        headline=['Abbildungsverzeichnis', 'Abbildungen'],
        blacklist=[
            'Inhalt',
            'Inhaltsverzeichnis',
            'Tabellen',
            'Tabellenverzeichnis',
        ],
        shortcut='figuretable',
    )
    return dumped
