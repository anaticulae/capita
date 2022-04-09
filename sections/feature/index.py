# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Index Page Detector
===================

Example
-------

    M
    Main text checklist, 131
    Masters degree, 4
        converting to doctoral thesis, 4
        examiners, 5
        full-time research, 5
        length, 5
        time-frame, 46
    Master version of text, 25
"""

import serializeraw
import utila

import sections.strategy


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages: tuple = None,
) -> str:
    """Load document and extract likelihood of beening an index page."""
    ptcns = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    dumped = sections.strategy.work(
        ptcns,
        headline=HEADLINES,
        noheadlines=None,
        pattern=INDEX_ITEM_PATTERN.match,
        shortcut='index',
        topsearch=False,
        second=True,
    )
    return dumped


HEADLINES = utila.splitlines("""
INDEX
""")

# INDEX, PAGENUMBER
INDEX_ITEM_PATTERN = utila.compiles(r"""
    ^
    ([A-Z]+\s?){1,3}                    # one till three words
    [\s|,]?                             # optional `,`
    \s{0,5}                             # between zero and five spaces
    (\d{1,3}[ ]{0,3}\,[ ]{0,3}){0,3}    # more optional page numbers
    [0-9]{1,4}$                         # a pagenumber at the end
""")
