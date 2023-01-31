# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Chapter Start Determination
===========================

Find the starts of a chapter.

What is typical for a start of chapter?

* Mostly there is a space between header and title start
* There is a number/chapter number
* There is a huge font
* The title is listed in table of content

1. Locate the distance between first line and header
2. Check the second line

QUESTIONS:

* TODO: Are chapters only content based or is appendix etc. a chapter too?
* TODO: REQUIRE APPROACH FOR SHORT PAPERS WIHTOUT CHPATER START AT TOP OF PAGE
"""

import iamraw
import serializeraw

import sections.chapter.run


def work(
    document: str,
    position: str,
    sizeandborder: str,
    footerheader: str,
    outlines: str,
    pages: tuple = None,
) -> str:
    """Determine likelihood of beeing a chapter startpage."""
    navigators = serializeraw.ptcn_fromfile(
        text=document,
        textpositions=position,
        sizeandborder=sizeandborder,
        headerfooter=footerheader,
        pages=pages,
    )
    outlines = load_outlines(outlines)
    # work
    result = sections.chapter.run.extract_chapter(
        navigators=navigators,
        outlines=outlines,
    )
    # write result
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def load_outlines(tocpath):
    """Load table of content out of outlines.

    Strip first outline wich is may the headline of the document.
    """
    toc = serializeraw.load_toc(tocpath)
    if len(toc) == 1:
        # maybe a headline
        toc: iamraw.Toc = iamraw.Toc(children=toc[0].children)
    return toc
