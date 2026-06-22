# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abstract Detector
=================
"""

import capita.feature
import capita.utils.headline
import configos
import elementae.headline.lookup
import serializeraw
import utilo

ABSTRACT_PAGE_MIN = configos.HV_INT_PLUS(default=0)

# TODO: MAKE THIS DOCUMENT LENGTH DEPENDENT!
ABSTRACT_PAGE_MAX = configos.HV_INT_PLUS(default=20)


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pdfinfo: str = None,
    pages=None,
) -> str:
    pages_max = None
    if utilo.exists(pdfinfo):
        pages_max = serializeraw.load_pdfinfo(pdfinfo).pages
    navigators = serializeraw.ptcn_fromfile(
        text=text_linewise,
        textpositions=textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooters,
        pages=pages_shrink(pages, pages_max=pages_max),
    )
    result = capita.feature.pagebypage(
        navigators,
        pageme=analyse_page,
        name='abstract',
    )
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def pages_shrink(pages: tuple, pages_max: int = None) -> tuple:
    """Allow abstract at the start and at the end of the document."""
    if not pages and not pages_max:
        return None
    pages = utilo.pages_inside(
        pages=pages,
        minn=ABSTRACT_PAGE_MIN,
        maxx=ABSTRACT_PAGE_MAX,
    )
    if pages_max is not None:
        morepages = utilo.pages_inside(
            pages=pages,
            minn=pages_max - ABSTRACT_PAGE_MAX,
            maxx=pages_max,
        )
        pages = pages + morepages
    pages = tuple(set(pages))
    return pages


def analyse_page(content):
    headlines = capita.utils.headline.headlines(
        content,
        topsearch=False,
        level_max=1,
    )
    if not headlines:
        return capita.feature.NO_PAGE
    if utilo.similar(
            expected=elementae.headline.lookup.ABSTRACT,
            current=headlines,
            maxdiff=0.95,
    ):
        return capita.feature.PERFECT
    return capita.feature.NO_PAGE
