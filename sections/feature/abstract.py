# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abstract Detector
=================
"""

import elements.headline.lookup
import serializeraw
import utila

import sections.feature
import sections.utils.headline

VALID_PAGES = utila.ranged_tuple(0, 20)


def work(
    text_linewise: str,
    textpositions: str,
    sizeandborder: str,
    headerfooters: str,
    pages=None,
) -> str:
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text_linewise,
        textpositions=textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooters,
        pages=pages,
    )
    result = sections.feature.pagebypage(
        navigators,
        pageme=analyse_page,
        name='abstract',
        minpage=0,
        maxpage=20,
    )
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = sections.utils.headline.headlines(
        content,
        topsearch=False,
        level_max=1,
    )
    if not headlines:
        return sections.feature.NO_PAGE
    if utila.similar(
            expected=elements.headline.lookup.ABSTRACT,
            current=headlines,
            maxdiff=0.95,
    ):
        return sections.feature.PERFECT
    return sections.feature.NO_PAGE
