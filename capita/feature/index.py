# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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
import utilo

import capita.strategy


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
        sizeandborder=sizeandborder,
        headerfooter=headerfooters,
        pages=pages,
    )
    dumped = capita.strategy.work(
        ptcns,
        headline=HEADLINES,
        noheadlines=None,
        pattern=INDEX_ITEM_PATTERN.match,
        shortcut='index',
        topsearch=False,
        second=True,
    )
    return dumped


HEADLINES = utilo.splitlines("""
INDEX
""")

# INDEX, PAGENUMBER
INDEX_ITEM_PATTERN = utilo.compiles(r"""
    ^
    ([A-Z]+\s?){1,3}                    # one till three words
    [\s|,]?                             # optional `,`
    \s{0,5}                             # between zero and five spaces
    (\d{1,3}[ ]{0,3}\,[ ]{0,3}){0,3}    # more optional page numbers
    [0-9]{1,4}$                         # a pagenumber at the end
""")
